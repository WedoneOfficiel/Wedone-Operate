"""Skill-oriented starting catalogue for French school levels.

This is a product taxonomy, not a claim that every listed objective is a
complete official curriculum mapping. Individual skills are enabled only when
a tested generator exists.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CurriculumLevel:
    id: str
    label: str
    cycle: str
    stage: str


@dataclass(frozen=True)
class Skill:
    id: str
    label: str
    level_id: str
    family: str
    operation: str
    objective: str
    min_difficulty: int = 1
    max_difficulty: int = 5
    enabled: bool = True


LEVELS = (
    CurriculumLevel("CP", "CP", "cycle2", "elementaire"),
    CurriculumLevel("CE1", "CE1", "cycle2", "elementaire"),
    CurriculumLevel("CE2", "CE2", "cycle2", "elementaire"),
    CurriculumLevel("CM1", "CM1", "cycle3", "elementaire"),
    CurriculumLevel("CM2", "CM2", "cycle3", "elementaire"),
    CurriculumLevel("6e", "6e", "cycle3", "college"),
    CurriculumLevel("5e", "5e", "cycle4", "college"),
    CurriculumLevel("4e", "4e", "cycle4", "college"),
    CurriculumLevel("3e", "3e", "cycle4", "college"),
    CurriculumLevel("2nde_GT", "Seconde générale et technologique", "lycee", "lycee"),
    CurriculumLevel("1re_GT", "Première générale et technologique", "lycee", "lycee"),
    CurriculumLevel("Tle_GT", "Terminale générale et technologique", "lycee", "lycee"),
)

# The first reliable engine slice covers integer mental calculation. More
# advanced objectives remain catalogue-only until their generators and
# correction rules have dedicated tests.
SKILLS = (
    Skill("cp.addition_20", "Additions jusqu'à 20", "CP", "calcul_mental", "addition", "Additionner deux nombres dont la somme ne dépasse pas 20."),
    Skill("cp.subtraction_20", "Soustractions jusqu'à 20", "CP", "calcul_mental", "subtraction", "Soustraire dans un domaine numérique allant jusqu'à 20."),
    Skill("ce1.addition_100", "Additions jusqu'à 100", "CE1", "calcul_mental", "addition", "Additionner des nombres à deux chiffres."),
    Skill("ce1.subtraction_100", "Soustractions jusqu'à 100", "CE1", "calcul_mental", "subtraction", "Soustraire des nombres à deux chiffres."),
    Skill("ce2.addition_1000", "Additions jusqu'à 1 000", "CE2", "calcul_mental", "addition", "Calculer des sommes dans le domaine des nombres jusqu'à 1 000."),
    Skill("ce2.multiplication_tables", "Tables de multiplication", "CE2", "automatismes", "multiplication", "Mémoriser et mobiliser les tables de multiplication."),
    Skill("cm1.multiplication", "Multiplications", "CM1", "calcul_mental", "multiplication", "Calculer des produits d'entiers."),
    Skill("cm2.division_exact", "Divisions exactes", "CM2", "automatismes", "division", "Mobiliser les relations entre multiplication et division."),
    Skill("college.signed_addition", "Addition de nombres relatifs", "5e", "calcul_numerique", "signed_addition", "Additionner des nombres relatifs."),
    Skill("college.signed_multiplication", "Multiplication de nombres relatifs", "4e", "calcul_numerique", "signed_multiplication", "Multiplier des nombres relatifs."),
    Skill("college.proportionality", "Proportionnalité", "4e", "proportionnalite", "proportionality", "Résoudre des calculs simples de proportionnalité.", enabled=False),
    Skill("lycee.fraction_calculation", "Calcul sur les fractions", "2nde_GT", "calcul_numerique", "fraction", "Effectuer des calculs sur les fractions.", enabled=False),
)

LEVEL_BY_ID = {level.id: level for level in LEVELS}
SKILL_BY_ID = {skill.id: skill for skill in SKILLS}


def skills_for_level(level_id: str, include_disabled: bool = False) -> tuple[Skill, ...]:
    if level_id not in LEVEL_BY_ID:
        raise ValueError(f"Niveau scolaire inconnu : {level_id}")
    return tuple(
        skill for skill in SKILLS
        if skill.level_id == level_id and (include_disabled or skill.enabled)
    )


def get_skill(skill_id: str) -> Skill:
    try:
        return SKILL_BY_ID[skill_id]
    except KeyError as exc:
        raise ValueError(f"Compétence inconnue : {skill_id}") from exc
