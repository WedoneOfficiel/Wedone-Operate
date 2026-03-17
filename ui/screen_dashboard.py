# ui/screen_dashboard.py — Wedone Operate
# Tableau de bord admin/prof : stats rapides + alertes élèves en difficulté.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
import database as db
import session
from constants import SCHOOL_LEVELS


class DashboardScreen(QWidget):
    open_admin    = pyqtSignal()
    open_stats    = pyqtSignal()
    open_settings = pyqtSignal()
    logout        = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # ── Barre du haut ──────────────────────────────────────────────
        topbar = QFrame()
        topbar.setFixedHeight(58)
        topbar.setStyleSheet("border-bottom: 1px solid rgba(128,128,128,0.12);")
        tl = QHBoxLayout(topbar); tl.setContentsMargins(28, 0, 28, 0)

        self.title_lbl = QLabel("Tableau de bord")
        self.title_lbl.setStyleSheet("font-size: 18px; font-weight: bold;")
        tl.addWidget(self.title_lbl); tl.addStretch()

        for label, signal in [
            ("🛠 Gestion",      self.open_admin),
            ("📊 Statistiques", self.open_stats),
            ("⚙ Paramètres",   self.open_settings),
            ("⬅ Déconnexion",  self.logout),
        ]:
            btn = QPushButton(label); btn.setProperty("class", "secondary")
            btn.clicked.connect(signal); tl.addWidget(btn)
        root.addWidget(topbar)

        # ── Contenu scrollable ─────────────────────────────────────────
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(28, 22, 28, 22)
        self.content_layout.setSpacing(20)
        scroll.setWidget(content)
        root.addWidget(scroll)

    def refresh(self):
        s = session.current
        self.title_lbl.setText(f"Tableau de bord — {s.display_name()}")
        self._clear()

        # ── Résumé rapide ──────────────────────────────────────────────
        summary_title = QLabel("Résumé")
        summary_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.content_layout.addWidget(summary_title)

        owner_id = None if s.is_admin() else s.user_id
        groups   = db.get_groups(owner_id=owner_id)
        all_students = []
        for g in groups:
            all_students.extend(db.get_students(group_id=g["id"]))

        total_sessions = sum(len(db.get_scores(st["id"])) for st in all_students)
        all_sc = db.get_all_scores()
        all_pcts = [sc["percent"] for sid in [st["id"] for st in all_students]
                    for sc in all_sc.get(sid, [])]
        avg_global = sum(all_pcts) / len(all_pcts) if all_pcts else None

        cards_row = QHBoxLayout(); cards_row.setSpacing(12)
        for value, label in [
            (str(len(groups)),        "groupe" + ("s" if len(groups) > 1 else "")),
            (str(len(all_students)),  "élève"  + ("s" if len(all_students) > 1 else "")),
            (str(total_sessions),     "session" + ("s" if total_sessions > 1 else "")),
            (f"{avg_global:.0f} %" if avg_global is not None else "—", "moyenne globale"),
        ]:
            card = self._stat_card(value, label)
            cards_row.addWidget(card)
        self.content_layout.addLayout(cards_row)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        self.content_layout.addWidget(sep)

        # ── Alertes élèves en difficulté ───────────────────────────────
        alert_title = QLabel("⚠  Élèves en difficulté")
        alert_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.content_layout.addWidget(alert_title)

        alert_subtitle = QLabel("Élèves avec une moyenne < 50 % sur leurs 3 dernières sessions")
        alert_subtitle.setObjectName("subtitle")
        self.content_layout.addWidget(alert_subtitle)

        all_alerts = []
        for g in groups:
            for alert in db.get_group_alerts(g["id"]):
                alert["group"] = g
                all_alerts.append(alert)

        if not all_alerts:
            ok_lbl = QLabel("✅  Aucun élève en difficulté — tout va bien !")
            ok_lbl.setStyleSheet("color: #1C8A4E; font-size: 14px; padding: 12px 0;")
            self.content_layout.addWidget(ok_lbl)
        else:
            for alert in all_alerts:
                self.content_layout.addWidget(self._alert_card(alert))

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        self.content_layout.addWidget(sep2)

        # ── Vue rapide par groupe ──────────────────────────────────────
        groups_title = QLabel("Aperçu des groupes")
        groups_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.content_layout.addWidget(groups_title)

        for g in groups:
            self.content_layout.addWidget(self._group_row(g))

        self.content_layout.addStretch()

    # ── Widgets ───────────────────────────────────────────────────────

    def _stat_card(self, value: str, label: str) -> QWidget:
        card = QFrame()
        card.setStyleSheet(
            "QFrame{background:var(--bg2,#F4F6F9);border:1px solid rgba(128,128,128,0.15);"
            "border-radius:10px;padding:4px;}"
        )
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        l = QVBoxLayout(card); l.setContentsMargins(16, 14, 16, 14); l.setSpacing(4)
        v = QLabel(value); v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.setStyleSheet("font-size: 28px; font-weight: bold; color: #0672BC;")
        lb = QLabel(label); lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lb.setObjectName("subtitle")
        l.addWidget(v); l.addWidget(lb)
        return card

    def _alert_card(self, alert: dict) -> QWidget:
        card = QFrame()
        card.setStyleSheet(
            "QFrame{background:#FFF5F5;border:1px solid #F5C1C1;border-radius:8px;}"
        )
        l = QHBoxLayout(card); l.setContentsMargins(14, 10, 14, 10); l.setSpacing(14)

        s = alert["student"]
        badge = QLabel(f"{s['prenom'][0]}{s['nom'][0]}".upper())
        badge.setFixedSize(36, 36)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet("background:#E05555;color:white;border-radius:18px;"
                            "font-size:13px;font-weight:bold;")
        l.addWidget(badge)

        info = QVBoxLayout(); info.setSpacing(2)
        name = QLabel(f"{s['prenom']} {s['nom']}")
        name.setStyleSheet("font-weight: bold; font-size: 14px;")
        detail = QLabel(
            f"Groupe : {alert['group']['name']}  •  "
            f"Moyenne : {alert['avg_percent']} %  •  "
            f"{alert['nb_sessions']} session{'s' if alert['nb_sessions'] > 1 else ''}"
        )
        detail.setObjectName("subtitle")
        info.addWidget(name); info.addWidget(detail)
        l.addLayout(info); l.addStretch()

        rec = alert["recommended"]
        rec_lbl = QLabel(f"💡 {rec['reason']}")
        rec_lbl.setStyleSheet("font-size: 12px; color: #9A6600;")
        rec_lbl.setWordWrap(True)
        rec_lbl.setMaximumWidth(280)
        l.addWidget(rec_lbl)
        return card

    def _group_row(self, g: dict) -> QWidget:
        row = QFrame()
        row.setStyleSheet(
            "QFrame{border:1px solid rgba(128,128,128,0.12);border-radius:8px;}"
        )
        l = QHBoxLayout(row); l.setContentsMargins(14, 10, 14, 10); l.setSpacing(16)

        name = QLabel(f"<b>{g['name']}</b>")
        name.setFixedWidth(160)
        l.addWidget(name)

        level_lbl = QLabel(g.get("level", "—"))
        level_lbl.setObjectName("subtitle")
        level_lbl.setFixedWidth(60)
        l.addWidget(level_lbl)

        students = db.get_students(group_id=g["id"])
        nb_s = len(students)
        sc_all = [sc for s in students for sc in db.get_scores(s["id"])]
        avg = sum(sc["percent"] for sc in sc_all) / len(sc_all) if sc_all else None

        nb_lbl = QLabel(f"{nb_s} élève{'s' if nb_s > 1 else ''}")
        nb_lbl.setObjectName("subtitle"); nb_lbl.setFixedWidth(80)
        l.addWidget(nb_lbl)

        if avg is not None:
            color = "#1C8A4E" if avg >= 70 else ("#E07B00" if avg >= 50 else "#C0392B")
            avg_lbl = QLabel(f"Moy. {avg:.0f} %")
            avg_lbl.setStyleSheet(f"font-weight: bold; color: {color};")
            l.addWidget(avg_lbl)

        l.addStretch()
        return row

    def _clear(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget(): sub.widget().deleteLater()
