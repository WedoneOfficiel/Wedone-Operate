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

import json, os, hashlib, uuid
from datetime import datetime
from constants import DEFAULT_ADMIN_PASSWORD_PLAIN, SCHOOL_LEVELS

USERS_FILE     = "users.json"
GROUPS_FILE    = "groups.json"
CLASSES_FILE   = "classes.json"
SCORES_FILE    = "scores.json"
TEMPLATES_FILE = "templates.json"

# ── Helpers ───────────────────────────────────────────────────────────

def _hash(p): return hashlib.sha256(p.encode()).hexdigest()
def _uid(prefix): return f"{prefix}_{uuid.uuid4().hex[:8]}"

def _load(path, default):
    if not os.path.exists(path): return default
    try:
        with open(path, "r", encoding="utf-8") as f: return json.load(f)
    except: return default

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Bootstrap users ───────────────────────────────────────────────────

def _load_users():
    default = {
        "admin": {"password_hash": _hash(DEFAULT_ADMIN_PASSWORD_PLAIN), "first_login": True},
        "teachers": [], "students": []
    }
    data = _load(USERS_FILE, default)
    data.setdefault("admin", default["admin"])
    data["admin"].setdefault("first_login", True)
    data.setdefault("teachers", []); data.setdefault("students", [])
    return data

def _save_users(data): _save(USERS_FILE, data)

# ══════════════════════════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════════════════════════

def check_admin_password(pwd): return _load_users()["admin"]["password_hash"] == _hash(pwd)
def set_admin_password(pwd):
    d = _load_users(); d["admin"]["password_hash"] = _hash(pwd); d["admin"]["first_login"] = False
    _save_users(d)
def is_admin_first_login(): return _load_users()["admin"].get("first_login", True)
def mark_admin_logged_in():
    d = _load_users(); d["admin"]["first_login"] = False; _save_users(d)

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
    d = _load_users()
    d["teachers"] = [t for t in d["teachers"] if t["id"] != tid]
    for s in d["students"]:
        if s.get("created_by") == tid: s["group_id"] = None
    _save_users(d)
    gs = _load(GROUPS_FILE, []); gs = [g for g in gs if g["owner_id"] != tid]; _save(GROUPS_FILE, gs)

def check_teacher_password(tid, pwd):
    t = get_teacher(tid); return t and t["password_hash"] == _hash(pwd)

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
    if owner_id: classes = [c for c in classes if c["owner_id"] == owner_id]
    return sorted(classes, key=lambda c: c["name"].lower())

def get_class(class_id):
    for c in _load(CLASSES_FILE, []):
        if c["id"] == class_id: return c
    return None

def add_class(name, owner_id):
    classes = _load(CLASSES_FILE, [])
    if any(c["name"].lower() == name.strip().lower() and c["owner_id"] == owner_id for c in classes): return None
    c = {"id": _uid("c"), "name": name.strip(), "owner_id": owner_id}
    classes.append(c); _save(CLASSES_FILE, classes); return c

def remove_class(class_id):
    classes = _load(CLASSES_FILE, [])
    classes = [c for c in classes if c["id"] != class_id]; _save(CLASSES_FILE, classes)
    # Délier les groupes de cette classe
    gs = _load(GROUPS_FILE, [])
    for g in gs:
        if g.get("class_id") == class_id: g["class_id"] = None
    _save(GROUPS_FILE, gs)

# ══════════════════════════════════════════════════════════════════════
# GROUPES (avec niveau scolaire + classe)
# ══════════════════════════════════════════════════════════════════════

def get_groups(owner_id=None, class_id=None):
    gs = _load(GROUPS_FILE, [])
    if owner_id: gs = [g for g in gs if g["owner_id"] == owner_id]
    if class_id: gs = [g for g in gs if g.get("class_id") == class_id]
    return sorted(gs, key=lambda g: g["name"].lower())

def get_group(gid):
    for g in _load(GROUPS_FILE, []): 
        if g["id"] == gid: return g
    return None

def add_group(name, owner_id, level="CM2", class_id=None):
    gs = _load(GROUPS_FILE, [])
    if any(g["name"].lower() == name.strip().lower() and g["owner_id"] == owner_id for g in gs): return None
    g = {"id": _uid("g"), "name": name.strip(), "owner_id": owner_id,
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
    gs = _load(GROUPS_FILE, [])
    gs = [g for g in gs if g["id"] != gid]; _save(GROUPS_FILE, gs)
    d = _load_users()
    for s in d["students"]:
        if s.get("group_id") == gid: s["group_id"] = None
    _save_users(d)

def get_group_level(gid):
    g = get_group(gid)
    return g["level"] if g else "CM2"

# ══════════════════════════════════════════════════════════════════════
# ÉLÈVES
# ══════════════════════════════════════════════════════════════════════

def get_students(teacher_id=None, group_id=None, class_id=None):
    d = _load_users(); students = d["students"]
    if teacher_id: students = [s for s in students if s.get("created_by") == teacher_id]
    if group_id:   students = [s for s in students if s.get("group_id") == group_id]
    if class_id:
        # Élèves dont le groupe appartient à cette classe
        gids = {g["id"] for g in get_groups(class_id=class_id)}
        students = [s for s in students if s.get("group_id") in gids]
    return sorted(students, key=lambda s: (s["nom"].lower(), s["prenom"].lower()))

def get_student(sid):
    for s in _load_users()["students"]:
        if s["id"] == sid: return s
    return None

def add_student(prenom, nom, teacher_id, group_id=None):
    d = _load_users()
    norm = (prenom.strip().lower(), nom.strip().lower())
    if any((s["prenom"].lower(), s["nom"].lower()) == norm for s in d["students"]): return None
    s = {"id": _uid("s"), "prenom": prenom.strip(), "nom": nom.strip(),
         "group_id": group_id, "created_by": teacher_id}
    d["students"].append(s); _save_users(d); return s

def remove_student(sid):
    d = _load_users()
    d["students"] = [s for s in d["students"] if s["id"] != sid]; _save_users(d)
    sc = _load(SCORES_FILE, {}); sc.pop(sid, None); _save(SCORES_FILE, sc)

def assign_student_group(sid, gid):
    d = _load_users()
    for s in d["students"]:
        if s["id"] == sid: s["group_id"] = gid; _save_users(d); return True
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
    ts = _load(TEMPLATES_FILE, [])
    if owner_id: ts = [t for t in ts if t["owner_id"] == owner_id]
    if group_id: ts = [t for t in ts if t.get("group_id") == group_id]
    return sorted(ts, key=lambda t: t["name"].lower())

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

def save_score(student_id, difficulty, total, correct, timer_enabled, operations, elapsed_seconds=None):
    sc = _load(SCORES_FILE, {})
    if student_id not in sc: sc[student_id] = []
    entry = {"date": datetime.now().isoformat(timespec="seconds"),
             "difficulty": difficulty, "total": total, "correct": correct,
             "percent": round(correct * 100 / total, 1) if total > 0 else 0,
             "timer_enabled": timer_enabled, "operations": operations}
    if elapsed_seconds is not None: entry["elapsed_seconds"] = round(elapsed_seconds, 1)
    sc[student_id].append(entry); _save(SCORES_FILE, sc)

def get_scores(student_id):
    return list(reversed(_load(SCORES_FILE, {}).get(student_id, [])))

def get_group_scores(group_id):
    students = get_students(group_id=group_id)
    all_sc = _load(SCORES_FILE, {})
    return {s["id"]: list(reversed(all_sc.get(s["id"], []))) for s in students}

def get_all_scores(): return _load(SCORES_FILE, {})

def export_group_csv(group_id):
    students = get_students(group_id=group_id)
    all_sc   = _load(SCORES_FILE, {})
    lines = ["Prénom,Nom,Date,Difficulté,Score,Total,Pourcentage,Chronométré,Durée(s)"]
    for s in students:
        for sc in all_sc.get(s["id"], []):
            lines.append(
                f"{s['prenom']},{s['nom']},{sc.get('date','')},{sc.get('difficulty','')},"
                f"{sc.get('correct','')},{sc.get('total','')},{sc.get('percent','')},"
                f"{'oui' if sc.get('timer_enabled') else 'non'},{sc.get('elapsed_seconds','')}"
            )
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════════════
# RECOMMANDATIONS AUTOMATIQUES
# ══════════════════════════════════════════════════════════════════════

def recommend_config_for_student(student_id: str) -> dict:
    """
    Analyse les dernières sessions d'un élève et propose une config adaptée.
    - < 50 % sur les 3 dernières sessions → baisser la difficulté
    - > 85 % → suggérer d'augmenter
    - Opérations ratées en priorité
    """
    scores = get_scores(student_id)[:5]   # 5 dernières
    level  = get_student_level(student_id)
    idx    = list(__import__("constants").SCHOOL_LEVELS).index(level) if level in __import__("constants").SCHOOL_LEVELS else 4

    if not scores:
        return {"level": level, "nb_epreuves": 10, "operations": ["addition","soustraction"],
                "timer_enabled": False, "reason": "Première session — configuration de départ."}

    avg_pct = sum(s["percent"] for s in scores) / len(scores)

    # Déterminer le niveau à proposer
    if avg_pct < 50 and idx > 0:
        suggested_level = __import__("constants").SCHOOL_LEVELS[idx - 1]
        reason = f"Moyenne récente {avg_pct:.0f} % — niveau abaissé pour consolider."
    elif avg_pct > 85 and idx < len(__import__("constants").SCHOOL_LEVELS) - 1:
        suggested_level = __import__("constants").SCHOOL_LEVELS[idx + 1]
        reason = f"Excellente moyenne {avg_pct:.0f} % — niveau augmenté pour progresser."
    else:
        suggested_level = level
        reason = f"Moyenne récente {avg_pct:.0f} % — niveau maintenu."

    # Opérations les moins réussies
    op_scores: dict = {}
    for s in scores:
        for op in s.get("operations", []):
            op_scores.setdefault(op, []).append(s["percent"])
    weak_ops = [op for op, vals in op_scores.items() if sum(vals)/len(vals) < 60]
    ops = weak_ops if weak_ops else ["addition", "soustraction", "multiplication", "division"]

    return {
        "level":         suggested_level,
        "nb_epreuves":   10,
        "operations":    ops,
        "timer_enabled": avg_pct > 75,
        "reason":        reason,
    }

def get_group_alerts(group_id: str) -> list[dict]:
    """
    Retourne la liste des élèves en difficulté dans un groupe.
    Critère : moyenne < 50 % sur les 3 dernières sessions.
    """
    alerts = []
    for s in get_students(group_id=group_id):
        scores = get_scores(s["id"])[:3]
        if not scores: continue
        avg = sum(sc["percent"] for sc in scores) / len(scores)
        if avg < 50:
            alerts.append({
                "student":     s,
                "avg_percent": round(avg, 1),
                "nb_sessions": len(get_scores(s["id"])),
                "recommended": recommend_config_for_student(s["id"]),
            })
    return sorted(alerts, key=lambda a: a["avg_percent"])
