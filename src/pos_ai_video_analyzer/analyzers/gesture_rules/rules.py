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
      if lndmk[poselandmark].visibility > 1.0000 or lndmk[poselandmark].visibility < 0.35:
        desconsiderar = True
    return desconsiderar

# Implementacao das Regras

class RegraBracoLevantado(GestureRule):
  def validate(self, lndmk):
    grau_satisfacao_regra = 0.08
    if ( not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.LEFT_ELBOW, PoseLandmark.LEFT_SHOULDER, PoseLandmark.LEFT_WRIST]) \
      and ( # validar se corpo está na vertical (não está deitado)
              (      lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y > 0.00 \
                and  lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 ) \
          or  (      lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y > 0.00 \
                and  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 ) \
        ) and ( 
              lndmk[PoseLandmark.LEFT_WRIST].y + grau_satisfacao_regra >= lndmk[PoseLandmark.LEFT_SHOULDER].y \
          or  (     lndmk[PoseLandmark.LEFT_ELBOW].y >= lndmk[PoseLandmark.LEFT_SHOULDER].y \
               and  lndmk[PoseLandmark.LEFT_WRIST].y > lndmk[PoseLandmark.LEFT_ELBOW].y ) \
        )) or ( \
      not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.RIGHT_ELBOW, PoseLandmark.RIGHT_SHOULDER, PoseLandmark.RIGHT_WRIST]) \
      and ( # validar se corpo está na vertical (não está deitado)
              (     lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y > 0.00 \
               and  lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y <= 0.2 ) \
          or  (     lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y > 0.00 \
               and  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y <= 0.2 ) \
        ) and ( # validar se pelo menos o pulso está mais alto que o ombro ou cotovelo
              lndmk[PoseLandmark.RIGHT_WRIST].y + grau_satisfacao_regra> lndmk[PoseLandmark.RIGHT_SHOULDER].y \
          or  (     lndmk[PoseLandmark.RIGHT_ELBOW].y > lndmk[PoseLandmark.RIGHT_SHOULDER].y \
               and  lndmk[PoseLandmark.RIGHT_WRIST].y > lndmk[PoseLandmark.RIGHT_ELBOW].y ) \
        )):
      return GestureRuleResult(True, 'BRACO_LEVANTADO', 'Braco levantado')
    return GestureRuleResult(False, '-', '-')

class RegraDeitado(GestureRule):
  def validate(self, lndmk):
    return GestureRuleResult(True, 'DEITADO', 'Posicao deitado ou na horizontal') \
      if not self.desconsiderar_validateavaliacao_regra(lndmk, [
        PoseLandmark.LEFT_SHOULDER, PoseLandmark.RIGHT_SHOULDER
      ]) \
        and (     lndmk[PoseLandmark.LEFT_SHOULDER].x - lndmk[PoseLandmark.RIGHT_SHOULDER].x <= 0.2 \
              or  lndmk[PoseLandmark.RIGHT_SHOULDER].x - lndmk[PoseLandmark.LEFT_SHOULDER].x <= 0.2 \
        ) \
        and (     lndmk[PoseLandmark.LEFT_SHOULDER].y - lndmk[PoseLandmark.RIGHT_SHOULDER].y > 0.6 \
              or  lndmk[PoseLandmark.RIGHT_SHOULDER].y - lndmk[PoseLandmark.LEFT_SHOULDER].y > 0.6 \
        ) else GestureRuleResult(False, '-', '-')
