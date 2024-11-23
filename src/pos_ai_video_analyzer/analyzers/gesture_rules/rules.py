from abc import ABC, abstractmethod
from mediapipe.python.solutions.pose import PoseLandmark

class GestureRuleResult:
  valid: bool
  name: str
  description: str

  def __init__(self, valid, name, description):
    self.valid = valid
    self.name = name
    self.description = description

  def is_valid(self):
    return self.valid

class GestureRule(ABC):

  @abstractmethod
  def validate(self, lndmk) -> GestureRuleResult:
    pass

  def desconsiderar_validateavaliacao_regra(self, lndmk, poselandmarks = []):
    desconsiderar = False
    for poselandmark in poselandmarks:
      if lndmk[poselandmark].visibility > 1.0000 or lndmk[poselandmark].visibility < 0.8000:
        desconsiderar = True
    return desconsiderar

# Implementacao das Regras

class RegraBracoEsquerdoLevantado(GestureRule):
  def validate(self, lndmk):
    if not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_WRIST]) \
      and lndmk[PoseLandmark.LEFT_ELBOW].y > lndmk[PoseLandmark.LEFT_SHOULDER].y \
      and lndmk[PoseLandmark.LEFT_WRIST].y > lndmk[PoseLandmark.LEFT_ELBOW].y \
      and lndmk[PoseLandmark.RIGHT_ELBOW].y <= lndmk[PoseLandmark.RIGHT_SHOULDER].y \
      and (
            lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 \
        or  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 \
      ):

      if lndmk[PoseLandmark.LEFT_SHOULDER].x > lndmk[PoseLandmark.RIGHT_SHOULDER].x:
        return GestureRuleResult(True, 'BRACO_LADO_ESQUERDO_LEVANTADO_DE_COSTAS', 'Braço lado esquerdo levantado (de costas)')
      else:
        return GestureRuleResult(True, 'BRACO_LADO_DIREITO_LEVANTADO', 'Braço lado direito levantado')
    return GestureRuleResult(False, '-', '-')


class RegraBracoDireitoLevantado(GestureRule):
  def validate(self, lndmk):
    if not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_WRIST]) \
      and lndmk[PoseLandmark.RIGHT_ELBOW].y > lndmk[PoseLandmark.RIGHT_SHOULDER].y \
      and lndmk[PoseLandmark.RIGHT_WRIST].y > lndmk[PoseLandmark.RIGHT_ELBOW].y \
      and lndmk[PoseLandmark.LEFT_ELBOW].y <= lndmk[PoseLandmark.LEFT_SHOULDER].y \
      and (
              lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 \
          or  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 \
        ):
      if lndmk[PoseLandmark.LEFT_SHOULDER].x > lndmk[PoseLandmark.RIGHT_SHOULDER].x:
        return GestureRuleResult(True, 'BRACO_LADO_DIREITO_LEVANTADO_DE_COSTAS', 'Braço lado direito levantado(de costas)')
      else:
        return GestureRuleResult(True, 'BRACO_LADO_ESQUERDO_LEVANTADO', 'Braço lado esquerdo levantado')
    return GestureRuleResult(False, '-', '-')

class RegraAmbosBracosLevantados(GestureRule):
  def validate(self, lndmk):
    if not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_WRIST,
        PoseLandmark.LEFT_ELBOW, PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER]) \
      and lndmk[PoseLandmark.LEFT_ELBOW].y > lndmk[PoseLandmark.LEFT_SHOULDER].y \
      and lndmk[PoseLandmark.LEFT_WRIST].y > lndmk[PoseLandmark.LEFT_ELBOW].y \
      and lndmk[PoseLandmark.RIGHT_ELBOW].y > lndmk[PoseLandmark.RIGHT_SHOULDER].y \
      and lndmk[PoseLandmark.LEFT_ELBOW].y <= lndmk[PoseLandmark.LEFT_SHOULDER].y \
      and (
              lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 \
          or  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 \
        ):
      if lndmk[PoseLandmark.LEFT_SHOULDER].x > lndmk[PoseLandmark.RIGHT_SHOULDER].x:
        return GestureRuleResult(True, 'BRACOS_LEVANTADOS_DE_COSTA', 'Braços levantados (de costa)')
      else:
        return GestureRuleResult(True, 'BRACOS_LEVANTADOS', 'Braços levantados')
    return GestureRuleResult(False, '-', '-')

# class RegraFazendoPoisSeMaoDireita(GestureRule):
#   def validate(self, lndmk):
#     return GestureRuleResult(True, 'POISE_MAO_DIREITA', 'Poisé com a mão direita') \
#       if not self.desconsiderar_validateavaliacao_regra(lndmk, [
#           PoseLandmark.RIGHT_THUMB, PoseLandmark.RIGHT_INDEX, PoseLandmark.RIGHT_PINKY,
#           PoseLandmark.RIGHT_WRIST]) \
#         and lndmk[PoseLandmark.RIGHT_THUMB].y > lndmk[PoseLandmark.RIGHT_INDEX].y \
#         and lndmk[PoseLandmark.RIGHT_THUMB].x >= lndmk[PoseLandmark.RIGHT_INDEX].x \
#         and lndmk[PoseLandmark.RIGHT_THUMB].x - 0.1 <= lndmk[PoseLandmark.RIGHT_INDEX].x \
#         and lndmk[PoseLandmark.RIGHT_THUMB].y > lndmk[PoseLandmark.RIGHT_PINKY].y \
#         and lndmk[PoseLandmark.RIGHT_THUMB].x >= lndmk[PoseLandmark.RIGHT_PINKY].x \
#         and lndmk[PoseLandmark.RIGHT_THUMB].x - 0.1 <= lndmk[PoseLandmark.RIGHT_PINKY].x \
#         and lndmk[PoseLandmark.RIGHT_THUMB].y > lndmk[PoseLandmark.RIGHT_WRIST].y \
#         and lndmk[PoseLandmark.RIGHT_WRIST].y + 0.5 >= lndmk[PoseLandmark.RIGHT_PINKY].y \
#       else GestureRuleResult(False, '-', '-')

# class RegraFazendoPoisSeMaoEsquerda(GestureRule):
#   def validate(self, lndmk):
#     return GestureRuleResult(True, 'POISE_MAO_ESQUERDA', 'Poisé com a mão esquerda') \
#       if not self.desconsiderar_validateavaliacao_regra(lndmk, [
#           PoseLandmark.LEFT_THUMB, PoseLandmark.LEFT_INDEX, PoseLandmark.LEFT_PINKY,
#           PoseLandmark.LEFT_WRIST]) \
#         and lndmk[PoseLandmark.LEFT_THUMB].y > lndmk[PoseLandmark.LEFT_INDEX].y \
#         and lndmk[PoseLandmark.LEFT_THUMB].y > lndmk[PoseLandmark.LEFT_PINKY].y \
#         and lndmk[PoseLandmark.LEFT_THUMB].y > lndmk[PoseLandmark.LEFT_WRIST].y \
#         and lndmk[PoseLandmark.LEFT_WRIST].y + 0.5 >= lndmk[PoseLandmark.LEFT_PINKY].y \
#         and lndmk[PoseLandmark.LEFT_WRIST].y + 0.5 <= lndmk[PoseLandmark.LEFT_PINKY].y + 0.5 \
#       else GestureRuleResult(False, '-', '-')

class RegraDeitado(GestureRule):
  def validate(self, lndmk):
    return GestureRuleResult(True, 'DEITADO', 'Posicao deitado ou na horizontal') \
      if not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER
      ]) \
        and (     lndmk[PoseLandmark.LEFT_SHOULDER].x - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 \
              or  lndmk[PoseLandmark.RIGHT_SHOULDER].x - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 \
        ) \
        and (     lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y > 0.6 \
              or  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y > 0.6 \
        ) else GestureRuleResult(False, '-', '-')
