# database.py — Wedone Operate
# Couche de données : users, classes, groupes (avec niveau scolaire),
# élèves, scores, modèles de session.
#
# Hiérarchie : Classe → Groupe (niveau scolaire) → Élèves
#
# users.json   : { admin, teachers[], students[] }
# groups.json  : [ { id, name, class_id, level, owner_id } ]
# classes.json : [ { id, name, owner_id } ]
# scores.json  : { student_id: [ session… ] }
# templates.json : [ { id, name, owner_id, group_id, config } ]

import json, os, hashlib, uuid, csv, io, tempfile, hmac, secrets
from data_paths import data_file
from datetime import datetime
from constants import SCHOOL_LEVELS

USERS_FILE     = "users.json"
GROUPS_FILE    = "groups.json"
CLASSES_FILE   = "classes.json"
SCORES_FILE    = "scores.json"
TEMPLATES_FILE = "templates.json"

# ── Helpers ───────────────────────────────────────────────────────────

def _hash(password):
    salt = secrets.token_bytes(16)
    iterations = 310_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return f"pbkdf2_sha256\u0024{iterations}\u0024{salt.hex()}\u0024{digest.hex()}"


def _verify_password(stored, password):
    if not stored or not isinstance(password, str):
        return False
    if stored.startswith("pbkdf2_sha256$"):
        try:
            _, iterations, salt_hex, digest_hex = stored.split("$", 3)
            digest = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, TypeError):
            return False
    # Backward compatibility: migrate legacy unsalted SHA-256 at next login.
    legacy = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(stored, legacy)

def _uid(prefix): return f"{prefix}_{uuid.uuid4().hex[:8]}"

class DataIntegrityError(RuntimeError):
    """Raised when a local data file exists but cannot safely be read."""


def _load(path, default):
    resolved = data_file(path)
    if not resolved.exists():
        return default
    try:
        with open(resolved, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        # Never silently replace unreadable user data with defaults on the
        # next write: that would turn a recoverable error into data loss.
        raise DataIntegrityError(
            f"Impossible de lire {resolved.name}. Le fichier original a été conservé."
        ) from exc


def _save(path, data):
    """Atomically replace a JSON file to avoid truncated data on interruption."""
    resolved = data_file(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        prefix=f".{resolved.name}.", suffix=".tmp", dir=str(resolved.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, resolved)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

# ── Bootstrap users ───────────────────────────────────────────────────

def _load_users():
    default = {"teachers": [], "students": []}
    data = _load(USERS_FILE, default)
    data.setdefault("teachers", [])
    data.setdefault("students", [])
    return data

def _save_users(data): _save(USERS_FILE, data)

# ══════════════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════════════

def check_admin_password(pwd):
    admin = _load_users().get("admin")
    if not admin or not _verify_password(admin.get("password_hash"), pwd):
        return False
    if not admin["password_hash"].startswith("pbkdf2_sha256$"):
        data = _load_users()
        data["admin"]["password_hash"] = _hash(pwd)
        _save_users(data)
    return True
def set_admin_password(pwd):
    d = _load_users()
    d.setdefault("admin", {})["password_hash"] = _hash(pwd)
    d["admin"]["first_login"] = False
    _save_users(d)
def is_admin_first_login(): return _load_users().get("admin", {}).get("first_login", False)
def mark_admin_logged_in():
    d = _load_users()
    if "admin" in d:
        d["admin"]["first_login"] = False
        _save_users(d)

# ══════════════════════════════════════════════════════════════════════
# PROFS
# ══════════════════════════════════════════════════════════════════════

def get_teachers(): return sorted(_load_users()["teachers"], key=lambda t:(t["nom"].lower(), t["prenom"].lower()))
def get_teacher(tid):
    for t in _load_users()["teachers"]:
        if t["id"] == tid: return t
    return None

def add_teacher(prenom, nom, password):
    d = _load_users()
    norm = (prenom.strip().lower(), nom.strip().lower())
    if any((t["prenom"].lower(), t["nom"].lower()) == norm for t in d["teachers"]): return None
    t = {"id": _uid("t"), "prenom": prenom.strip(), "nom": nom.strip(),
         "password_hash": _hash(password), "first_login": True}
    d["teachers"].append(t); _save_users(d); return t

def remove_teacher(tid):
    """Remove a teacher profile but keep student identities and score history.

    Orphaned students are moved to the local guest workspace so they remain
    accessible instead of being silently stranded behind a deleted account.
    """
    users = _load_users()
    users["teachers"] = [teacher for teacher in users["teachers"] if teacher["id"] != tid]
    for student in users["students"]:
        if student.get("created_by") == tid:
            student["created_by"] = "guest"
            student["group_id"] = None
            student["class_id"] = None
    _save_users(users)

    groups = _load(GROUPS_FILE, [])
    _save(GROUPS_FILE, [group for group in groups if group.get("owner_id") != tid])
    classes = _load(CLASSES_FILE, [])
    _save(CLASSES_FILE, [cls for cls in classes if cls.get("owner_id") != tid])
    templates = _load(TEMPLATES_FILE, [])
    _save(TEMPLATES_FILE, [template for template in templates if template.get("owner_id") != tid])

def check_teacher_password(tid, pwd):
    teacher = get_teacher(tid)
    if not teacher or not _verify_password(teacher.get("password_hash"), pwd):
        return False
    if not teacher["password_hash"].startswith("pbkdf2_sha256$"):
        users = _load_users()
        for item in users["teachers"]:
            if item["id"] == tid:
                item["password_hash"] = _hash(pwd)
                break
        _save_users(users)
    return True

def set_teacher_password(tid, pwd):
    d = _load_users()
    for t in d["teachers"]:
        if t["id"] == tid: t["password_hash"] = _hash(pwd); t["first_login"] = False; _save_users(d); return True
    return False

def is_teacher_first_login(tid):
    t = get_teacher(tid); return t.get("first_login", False) if t else False

def teacher_full_name(t): return f"{t['prenom']} {t['nom']}"

# ══════════════════════════════════════════════════════════════════════
# CLASSES
# ══════════════════════════════════════════════════════════════════════

def get_classes(owner_id=None):
    classes = _load(CLASSES_FILE, [])
    if owner_id is not None:
        classes = [c for c in classes if c.get("owner_id") == owner_id]
    return sorted(classes, key=lambda c: c["name"].lower())

def get_class(class_id):
    for c in _load(CLASSES_FILE, []):
        if c["id"] == class_id: return c
    return None

def add_class(name, owner_id):
    name = name.strip()
    if not name or owner_id is None:
        return None
    classes = _load(CLASSES_FILE, [])
    if any(c["name"].casefold() == name.casefold() and c.get("owner_id") == owner_id for c in classes): return None
    c = {"id": _uid("c"), "name": name, "owner_id": owner_id}
    classes.append(c); _save(CLASSES_FILE, classes); return c

def remove_class(class_id):
    """Remove a class while preserving students and their score history."""
    classes = _load(CLASSES_FILE, [])
    classes = [c for c in classes if c["id"] != class_id]
    _save(CLASSES_FILE, classes)
    # Groups and students remain usable as unassigned records.
    gs = _load(GROUPS_FILE, [])
    for g in gs:
        if g.get("class_id") == class_id:
            g["class_id"] = None
    _save(GROUPS_FILE, gs)
    users = _load_users()
    for student in users["students"]:
        if student.get("class_id") == class_id:
            student["class_id"] = None
    _save_users(users)

# ══════════════════════════════════════════════════════════════════════
# GROUPES (avec niveau scolaire + classe)
# ══════════════════════════════════════════════════════════════════════

def get_groups(owner_id=None, class_id=None):
    groups = _load(GROUPS_FILE, [])
    if owner_id is not None:
        groups = [g for g in groups if g.get("owner_id") == owner_id]
    if class_id is not None:
        groups = [g for g in groups if g.get("class_id") == class_id]
    return sorted(groups, key=lambda g: g.get("name", "").casefold())

def get_group(gid):
    for g in _load(GROUPS_FILE, []): 
        if g["id"] == gid: return g
    return None

def add_group(name, owner_id, level="CM2", class_id=None):
    name = name.strip()
    if not name or owner_id is None or level not in SCHOOL_LEVELS:
        return None
    if class_id:
        cls = get_class(class_id)
        if not cls or cls.get("owner_id") != owner_id:
            return None
    gs = _load(GROUPS_FILE, [])
    if any(g["name"].casefold() == name.casefold() and g.get("owner_id") == owner_id for g in gs): return None
    g = {"id": _uid("g"), "name": name, "owner_id": owner_id,
         "level": level, "class_id": class_id}
    gs.append(g); _save(GROUPS_FILE, gs); return g

def update_group(gid, **kwargs):
    gs = _load(GROUPS_FILE, [])
    for g in gs:
        if g["id"] == gid:
            for k, v in kwargs.items(): g[k] = v
            _save(GROUPS_FILE, gs); return True
    return False

def remove_group(gid):
    groups = _load(GROUPS_FILE, [])
    removed = next((group for group in groups if group["id"] == gid), None)
    _save(GROUPS_FILE, [group for group in groups if group["id"] != gid])
    users = _load_users()
    for student in users["students"]:
        if student.get("group_id") == gid:
            student["group_id"] = None
            if removed and removed.get("class_id"):
                student["class_id"] = removed["class_id"]
    _save_users(users)
    # Detach reusable templates rather than leaving dangling group references.
    templates = _load(TEMPLATES_FILE, [])
    for template in templates:
        if template.get("group_id") == gid:
            template["group_id"] = None
    _save(TEMPLATES_FILE, templates)

def get_group_level(gid):
    g = get_group(gid)
    return g["level"] if g else "CM2"

# ══════════════════════════════════════════════════════════════════════
# ÉLÈVES
# ══════════════════════════════════════════════════════════════════════

def get_students(teacher_id=None, group_id=None, class_id=None):
    students = _load_users()["students"]
    if teacher_id is not None:
        students = [s for s in students if s.get("created_by") == teacher_id]
    if group_id is not None:
        students = [s for s in students if s.get("group_id") == group_id]
    if class_id:
        # Include both students assigned directly to a class and students
        # whose optional group belongs to that class.
        group_ids = {g["id"] for g in get_groups(class_id=class_id)}
        students = [
            s for s in students
            if s.get("class_id") == class_id or s.get("group_id") in group_ids
        ]
    return sorted(
        students,
        key=lambda s: (s.get("nom", "").casefold(), s.get("prenom", "").casefold())
    )

def get_student(sid):
    for s in _load_users()["students"]:
        if s["id"] == sid: return s
    return None

def add_student(prenom, nom, teacher_id, group_id=None, class_id=None):
    d = _load_users()
    prenom, nom = prenom.strip(), nom.strip()
    if not prenom or not nom:
        return None
    norm = (prenom.casefold(), nom.casefold())
    # Identical names are valid in different teacher workspaces.
    if any(
        (s.get("prenom", "").casefold(), s.get("nom", "").casefold()) == norm
        and s.get("created_by") == teacher_id
        for s in d["students"]
    ):
        return None
    if group_id:
        group = get_group(group_id)
        if not group or (teacher_id and group.get("owner_id") != teacher_id):
            return None
        if class_id and group.get("class_id") not in (None, class_id):
            return None
        class_id = class_id or group.get("class_id")
    student = {
        "id": _uid("s"), "prenom": prenom, "nom": nom,
        "group_id": group_id, "class_id": class_id, "created_by": teacher_id
    }
    d["students"].append(student)
    _save_users(d)
    return student


def assign_student_class(student_id, class_id):
    """Assign a student directly to a class, without requiring a group."""
    if class_id and not get_class(class_id):
        return False
    users = _load_users()
    for student in users["students"]:
        if student["id"] == student_id:
            student["class_id"] = class_id
            # A direct class assignment is distinct from group membership.
            if student.get("group_id"):
                group = get_group(student["group_id"])
                if group and class_id and group.get("class_id") not in (None, class_id):
                    return False
            _save_users(users)
            return True
    return False

def remove_student(sid):
    d = _load_users()
    d["students"] = [s for s in d["students"] if s["id"] != sid]; _save_users(d)
    sc = _load(SCORES_FILE, {}); sc.pop(sid, None); _save(SCORES_FILE, sc)

def assign_student_group(sid, gid):
    group = get_group(gid) if gid else None
    if gid and not group:
        return False
    users = _load_users()
    for student in users["students"]:
        if student["id"] == sid:
            if group and student.get("created_by") not in (None, "guest", group.get("owner_id")):
                return False
            student["group_id"] = gid
            if group and group.get("class_id"):
                student["class_id"] = group["class_id"]
            _save_users(users)
            return True
    return False

def student_full_name(s): return f"{s['prenom']} {s['nom']}"

def get_student_level(sid):
    """Retourne le niveau scolaire de l'élève via son groupe."""
    s = get_student(sid)
    if not s or not s.get("group_id"): return "CM2"
    return get_group_level(s["group_id"])

# ══════════════════════════════════════════════════════════════════════
# MODÈLES DE SESSION
# ══════════════════════════════════════════════════════════════════════

def get_templates(owner_id=None, group_id=None):
    templates = _load(TEMPLATES_FILE, [])
    if owner_id is not None:
        templates = [t for t in templates if t.get("owner_id") == owner_id]
    if group_id is not None:
        templates = [t for t in templates if t.get("group_id") == group_id]
    return sorted(templates, key=lambda t: t.get("name", "").casefold())

def get_template(tid):
    for t in _load(TEMPLATES_FILE, []):
        if t["id"] == tid: return t
    return None

def save_template(name, owner_id, config, group_id=None):
    """Crée ou met à jour un modèle de session."""
    ts = _load(TEMPLATES_FILE, [])
    existing = next((t for t in ts if t["owner_id"] == owner_id
                     and t["name"].lower() == name.strip().lower()), None)
    if existing:
        existing["config"] = config; existing["group_id"] = group_id
    else:
        ts.append({"id": _uid("tm"), "name": name.strip(),
                   "owner_id": owner_id, "group_id": group_id, "config": config})
    _save(TEMPLATES_FILE, ts)

def remove_template(tid):
    ts = _load(TEMPLATES_FILE, [])
    ts = [t for t in ts if t["id"] != tid]; _save(TEMPLATES_FILE, ts)

def get_group_default_template(group_id):
    """Retourne le modèle assigné à ce groupe, ou None."""
    ts = get_templates(group_id=group_id)
    return ts[0] if ts else None

# ══════════════════════════════════════════════════════════════════════
# SCORES
# ══════════════════════════════════════════════════════════════════════

def save_score(student_id, difficulty, total, correct, timer_enabled, operations, elapsed_seconds=None, details=None):
    if not student_id:
        raise ValueError("student_id est obligatoire")
    if not isinstance(total, int) or total <= 0:
        raise ValueError("total doit être un entier strictement positif")
    if not isinstance(correct, int) or not 0 <= correct <= total:
        raise ValueError("correct doit être compris entre 0 et total")
    sc = _load(SCORES_FILE, {})
    if student_id not in sc: sc[student_id] = []
    entry = {"date": datetime.now().isoformat(timespec="seconds"),
             "difficulty": difficulty, "total": total, "correct": correct,
             "percent": round(correct * 100 / total, 1) if total > 0 else 0,
             "timer_enabled": bool(timer_enabled), "operations": list(operations or [])}
    if elapsed_seconds is not None:
        entry["elapsed_seconds"] = round(max(0, float(elapsed_seconds)), 1)
    if details is not None:
        entry["details"] = details
    sc[student_id].append(entry); _save(SCORES_FILE, sc)

def get_scores(student_id):
    return list(reversed(_load(SCORES_FILE, {}).get(student_id, [])))

def get_group_scores(group_id):
    return get_students_scores([student["id"] for student in get_students(group_id=group_id)])


def get_students_scores(student_ids):
    all_scores = _load(SCORES_FILE, {})
    return {
        student_id: list(reversed(all_scores.get(student_id, [])))
        for student_id in student_ids
    }

def get_all_scores(): return _load(SCORES_FILE, {})

def export_group_csv(group_id):
    return export_students_csv(get_students(group_id=group_id))


def export_class_csv(class_id):
    return export_students_csv(get_students(class_id=class_id))


def export_students_csv(students):
    all_scores = _load(SCORES_FILE, {})
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Prénom", "Nom", "Date", "Niveau", "Score", "Total",
                     "Pourcentage", "Chronométré", "Durée(s)"])
    for student in students:
        for score in all_scores.get(student["id"], []):
            writer.writerow([
                student.get("prenom", ""), student.get("nom", ""),
                score.get("date", ""), score.get("difficulty", ""),
                score.get("correct", ""), score.get("total", ""),
                score.get("percent", ""),
                "oui" if score.get("timer_enabled") else "non",
                score.get("elapsed_seconds", "")
            ])
    return output.getvalue()


def recommend_config_for_student(student_id: str) -> dict:
    """Suggest a cautious next session from recent, question-level evidence."""
    scores = get_scores(student_id)[:5]
    level = get_student_level(student_id)
    levels = SCHOOL_LEVELS
    idx = levels.index(level) if level in levels else levels.index("CM2")

    if not scores:
        return {
            "level": level, "nb_epreuves": 10,
            "operations": ["addition", "soustraction"],
            "timer_enabled": False,
            "reason": "Première session : commencer sans chronomètre et observer les résultats."
        }

    # Weight sessions by the number of questions, rather than averaging session
    # percentages equally (a 1-question session should not weigh like 30).
    total_questions = sum(max(0, int(s.get("total", 0))) for s in scores)
    total_correct = sum(max(0, int(s.get("correct", 0))) for s in scores)
    avg_pct = (total_correct * 100 / total_questions) if total_questions else 0.0

    suggested_level = level
    reason = f"Résultats récents : {avg_pct:.0f} % — niveau maintenu."
    if len(scores) >= 3 and avg_pct < 45 and idx > 0:
        suggested_level = levels[idx - 1]
        reason = f"Résultats récents : {avg_pct:.0f} % — proposer un niveau inférieur pour consolider."
    elif len(scores) >= 3 and avg_pct >= 90 and idx < len(levels) - 1:
        suggested_level = levels[idx + 1]
        reason = f"Résultats récents : {avg_pct:.0f} % — proposer un niveau supérieur."

    # New sessions persist per-question operations. Older history gracefully
    # falls back to session-level operation labels without pretending to know
    # which operation caused each error.
    operation_totals = {}
    for score in scores:
        for detail in score.get("details", []):
            op = detail.get("operation")
            if op in ("addition", "soustraction", "multiplication", "division"):
                bucket = operation_totals.setdefault(op, {"correct": 0, "total": 0})
                bucket["total"] += 1
                bucket["correct"] += int(bool(detail.get("correct")))
    weak_ops = [
        op for op, stats in operation_totals.items()
        if stats["total"] >= 3 and stats["correct"] / stats["total"] < 0.6
    ]
    if weak_ops:
        operations = weak_ops
        operation_reason = "Priorité aux opérations les moins maîtrisées."
    else:
        operations = list(dict.fromkeys(scores[0].get("operations", [])))
        if not operations:
            operations = ["addition", "soustraction"]
        operation_reason = "Conserver les opérations travaillées récemment."

    return {
        "level": suggested_level,
        "nb_epreuves": 10,
        "operations": operations,
        # Do not enable a timer from accuracy alone: speed is a separate skill.
        "timer_enabled": False,
        "reason": reason + " " + operation_reason,
        "recent_accuracy": round(avg_pct, 1),
        "evidence_sessions": len(scores),
    }


def get_student_alerts(student_ids=None) -> list[dict]:
    """Return cautious support alerts for a supplied set of students."""
    students = _load_users()["students"]
    if student_ids is not None:
        wanted = set(student_ids)
        students = [student for student in students if student["id"] in wanted]
    alerts = []
    for student in students:
        scores = get_scores(student["id"])[:3]
        if len(scores) < 2:
            continue
        total = sum(max(0, int(score.get("total", 0))) for score in scores)
        correct = sum(max(0, int(score.get("correct", 0))) for score in scores)
        if not total:
            continue
        avg = correct * 100 / total
        if avg < 50:
            group = get_group(student.get("group_id")) if student.get("group_id") else None
            alerts.append({
                "student": student,
                "group": group,
                "avg_percent": round(avg, 1),
                "nb_sessions": len(get_scores(student["id"])),
                "recommended": recommend_config_for_student(student["id"]),
            })
    return sorted(alerts, key=lambda alert: alert["avg_percent"])


def get_group_alerts(group_id: str) -> list[dict]:
    """Compatibility wrapper for older UI screens."""
    return get_student_alerts([student["id"] for student in get_students(group_id=group_id)])
