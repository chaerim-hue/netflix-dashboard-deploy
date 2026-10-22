# ABA3 Netflix TOP 10 Dashboard

기존 분석의 집계 결과와 비공식 AI 브랜드 비주얼을 표시하는 공개 배포용 앱입니다.
모델 학습·예측 재계산·AI 생성·인증키가 필요하지 않습니다.

## 로컬 실행

Python 3.12 환경을 권장합니다. 폴더 루트에서 실행합니다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r dashboard/requirements.txt
python -m streamlit run dashboard/app.py
```

Windows에서는 `.venv\Scripts\Activate.ps1`로 활성화합니다.
패키지는 검증된 Streamlit 1.50.0 / pandas 2.3.3 / Pillow 11.3.0 / Altair 5.5.0을 유지합니다.
macOS Python 3.9.6 실행 검증과 Cloud Linux/Python 3.12 실행 검증은 구분합니다.

## Streamlit Community Cloud 설정

GitHub 공개 저장소 준비 후 Main file path는 `dashboard/app.py`, Python은 3.12로 선택합니다.
의존성은 `dashboard/requirements.txt`, 테마는 루트 `.streamlit/config.toml`을 사용합니다.
인증정보 설정은 필요 없습니다. 이 폴더 준비 과정에서는 저장소 생성·Commit·Push·Deploy를 하지 않았습니다.

## 해석 범위

수업 제공 29주 데이터의 저장된 결과를 사용합니다. 학습251·검증60·기존 평가46개입니다.
개선 log1p Ridge의 독립 최종평가는 미실시입니다. 검증 예측 기반 후보는 사례 연구입니다.
두 AI 로고는 공식 Netflix 캠페인·공식 로고가 아니며 홍보 효과를 측정하지 않았습니다.
원본 데이터·개별 예측·모델·연구 코드·로컬 전용 자료는 포함하지 않았습니다.
공개 배포용 복사본 제공은 제3자 상표·이미지의 별도 이용 허가를 의미하지 않습니다.
