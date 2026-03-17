# ui/screen_stats.py — Wedone Operate
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QComboBox, QFileDialog, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
import database as db
import session


class StatsScreen(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 26, 36, 26); root.setSpacing(14)

        header = QHBoxLayout()
        self.title_label = QLabel("Statistiques")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header.addWidget(self.title_label); header.addStretch()
        back_btn = QPushButton("← Retour"); back_btn.setProperty("class", "secondary")
        back_btn.clicked.connect(self.go_back); header.addWidget(back_btn)
        root.addLayout(header)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); root.addWidget(sep)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_personal_tab(), "📈 Mes sessions")
        self.tabs.addTab(self._build_group_tab(),    "👥 Groupe")
        root.addWidget(self.tabs)

    def _build_personal_tab(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 12, 0, 0); l.setSpacing(10)
        self.personal_summary = QLabel(""); self.personal_summary.setObjectName("subtitle")
        l.addWidget(self.personal_summary)
        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.personal_container = QWidget()
        self.personal_layout = QVBoxLayout(self.personal_container)
        self.personal_layout.setSpacing(8); self.personal_layout.setContentsMargins(0,0,0,0)
        scroll.setWidget(self.personal_container); l.addWidget(scroll)
        return w

    def _build_group_tab(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.setContentsMargins(0, 12, 0, 0); l.setSpacing(10)

        sel_row = QHBoxLayout()
        sel_row.addWidget(QLabel("Groupe :"))
        self.group_selector = QComboBox(); self.group_selector.setFixedWidth(220)
        self.group_selector.currentIndexChanged.connect(self._refresh_group_stats)
        sel_row.addWidget(self.group_selector); sel_row.addStretch()
        export_btn = QPushButton("⬇ Exporter CSV"); export_btn.setProperty("class", "secondary")
        export_btn.clicked.connect(self._export_csv); sel_row.addWidget(export_btn)
        l.addLayout(sel_row)

        self.group_summary = QLabel(""); self.group_summary.setObjectName("subtitle")
        l.addWidget(self.group_summary)

        self.group_table = QTableWidget()
        self.group_table.setColumnCount(5)
        self.group_table.setHorizontalHeaderLabels(["Élève","Sessions","Moyenne","Meilleur","Dernier"])
        self.group_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.group_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.group_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        l.addWidget(self.group_table)
        return w

    def refresh(self):
        s = session.current
        self.title_label.setText(f"Statistiques — {s.display_name()}" if s.is_student() else "Statistiques")
        self._refresh_personal()
        self._refresh_group_selector()
        self.tabs.setTabVisible(1, s.can_see_group_stats())

    def _refresh_personal(self):
        sid = session.current.user_id
        self._clear(self.personal_layout)
        if not sid:
            self.personal_summary.setText("Connecté en tant qu'admin."); return
        scores = db.get_scores(sid)
        if not scores:
            self.personal_summary.setText("Aucune session enregistrée.")
            lbl = QLabel("Pas encore de session jouée !")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl.setObjectName("subtitle")
            self.personal_layout.addWidget(lbl); self.personal_layout.addStretch(); return
        avg = sum(s["percent"] for s in scores) / len(scores)
        best = max(scores, key=lambda s: s["percent"])
        self.personal_summary.setText(
            f"{len(scores)} session{'s' if len(scores)>1 else ''}  •  "
            f"Moyenne : {avg:.1f} %  •  Meilleur : {best['percent']:.1f} %"
        )
        for s in scores: self.personal_layout.addWidget(self._make_card(s))
        self.personal_layout.addStretch()

    def _refresh_group_selector(self):
        self.group_selector.blockSignals(True); self.group_selector.clear()
        owner_id = None if session.current.is_admin() else session.current.user_id
        for g in db.get_groups(owner_id=owner_id):
            self.group_selector.addItem(g["name"], userData=g["id"])
        self.group_selector.blockSignals(False)
        self._refresh_group_stats()

    def _refresh_group_stats(self):
        group_id = self.group_selector.currentData()
        if not group_id:
            self.group_summary.setText("Aucun groupe disponible."); self.group_table.setRowCount(0); return
        students = db.get_students(group_id=group_id)
        all_scores = db.get_group_scores(group_id)
        if not students:
            self.group_summary.setText("Aucun élève dans ce groupe."); self.group_table.setRowCount(0); return

        avgs = []; self.group_table.setRowCount(len(students))
        for row, s in enumerate(students):
            sc = all_scores.get(s["id"], [])
            nb = len(sc)
            avg = sum(x["percent"] for x in sc) / nb if nb else 0
            best = max((x["percent"] for x in sc), default=0)
            last = sc[0]["percent"] if sc else None
            avgs.append(avg)
            self.group_table.setItem(row, 0, QTableWidgetItem(f"{s['prenom']} {s['nom']}"))
            self.group_table.setItem(row, 1, QTableWidgetItem(str(nb)))
            self.group_table.setItem(row, 2, QTableWidgetItem(f"{avg:.1f} %" if nb else "—"))
            self.group_table.setItem(row, 3, QTableWidgetItem(f"{best:.1f} %" if nb else "—"))
            self.group_table.setItem(row, 4, QTableWidgetItem(f"{last:.1f} %" if last is not None else "—"))

        group = db.get_group(group_id)
        self.group_summary.setText(
            f"Groupe « {group['name'] if group else ''} »  •  "
            f"{len(students)} élève{'s' if len(students)>1 else ''}  •  "
            f"Moyenne : {(sum(avgs)/len(avgs)):.1f} %"
        )

    def _export_csv(self):
        group_id = self.group_selector.currentData()
        if not group_id: return
        group = db.get_group(group_id)
        name = f"stats_{group['name'].replace(' ','_')}.csv" if group else "stats.csv"
        path, _ = QFileDialog.getSaveFileName(self, "Exporter", name, "CSV (*.csv)")
        if path:
            with open(path, "w", encoding="utf-8-sig") as f:
                f.write(db.export_group_csv(group_id))

    def _make_card(self, s: dict) -> QWidget:
        card = QFrame()
        card.setStyleSheet("QFrame{border:1px solid rgba(128,128,128,0.18);border-radius:8px;padding:2px;}")
        l = QHBoxLayout(card); l.setSpacing(18)
        pct = s.get("percent", 0)
        color = "#2EBD6E" if pct >= 80 else ("#F0A030" if pct >= 50 else "#E05555")
        ops_map = {"addition":"+","soustraction":"−","multiplication":"×","division":"÷"}
        for text, w in [(s.get("date","")[:10], 90), (s.get("difficulty",""), 80),
                        (" ".join(ops_map.get(o,o) for o in s.get("operations",[])), 80)]:
            lbl = QLabel(text); lbl.setFixedWidth(w); lbl.setObjectName("subtitle"); l.addWidget(lbl)
        score_lbl = QLabel(f"{s['correct']}/{s['total']}  —  {pct:.1f} %")
        score_lbl.setStyleSheet(f"font-weight:bold;color:{color};"); l.addWidget(score_lbl)
        if s.get("elapsed_seconds") is not None:
            e = s["elapsed_seconds"]
            l.addWidget(QLabel(f"⏱ {int(e)//60}m{int(e)%60:02d}s"))
        l.addStretch()
        return card

    def _clear(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
