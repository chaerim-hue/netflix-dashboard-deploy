"""Read-only dashboard of the frozen ABA3 analysis and generated visual assets."""
from pathlib import Path
import json
import altair as alt
import pandas as pd
from PIL import Image
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parent / 'data'
TABLES = ROOT / 'reports/tables'
ASSETS = {
    'eda': ROOT / 'reports/figures/course-eda-2week-2026-10-15/training_relationships.png',
    'insights': ROOT / 'reports/figures/course-log1p-business-insights-2026-10-19/prediction_actual_and_groups.png',
    'red_notice': ROOT / 'reports/final/ai-logo-assets/red_notice_ai_logo.png',
    'hellbound': ROOT / 'reports/final/ai-logo-assets/hellbound_s1_ai_logo.png',
}


def load_results():
    """Only aggregate CSVs, the approved public summary and final PNGs are read."""
    baseline = pd.read_csv(TABLES / 'course-baseline-ridge-2026-10-15/metrics.csv', encoding='utf-8-sig')
    improved = pd.read_csv(TABLES / 'course-ridge-log1p-validation-2026-10-19/metrics.csv', encoding='utf-8-sig')
    ranks = pd.read_csv(TABLES / 'course-eda-2week-2026-10-15/train_rank.csv', encoding='utf-8-sig')
    targets = pd.read_csv(TABLES / 'course-eda-2week-2026-10-15/train_target_distribution.csv', encoding='utf-8-sig')
    groups = pd.read_csv(TABLES / 'course-log1p-business-insights-2026-10-19/prediction_groups.csv', encoding='utf-8-sig')
    top3 = json.loads((DATA / 'top3_summary.json').read_text(encoding='utf-8'))['candidates']
    for name, path in ASSETS.items():
        with Image.open(path) as image:
            if image.format != 'PNG':
                raise ValueError('PNG 형식이 아닙니다: ' + path.name)
            if name in ('red_notice', 'hellbound') and image.size != (1024, 1024):
                raise ValueError('로고 규격이 1024×1024가 아닙니다: ' + path.name)
            image.verify()
        with Image.open(path) as image:
            image.load()
    val = baseline.loc[baseline['partition'] == 'validation'].iloc[0]
    test = baseline.loc[baseline['partition'] == 'test'].iloc[0]
    log = improved.loc[improved['partition'] == 'validation'].iloc[0]
    if int(val['n']) != 60 or int(test['n']) != 46 or int(log['n']) != 60 or int(targets['n'].sum()) != 251:
        raise ValueError('저장된 표본 수가 확정 분석 기준과 다릅니다.')
    return dict(val=val, test=test, log=log, ranks=ranks, targets=targets, groups=groups, top3=top3)


def main():
    st.set_page_config(page_title='ABA3 | Netflix Data × AI Visual', page_icon='🎬', layout='wide')
    st.markdown('''<style>
    .block-container {max-width:1160px;padding-top:2rem;padding-bottom:4rem;}
    h1 {letter-spacing:-.04em;} h2 {padding-top:1.2rem;}
    [data-testid="stMetric"] {background:#18181f;border:1px solid #303039;border-radius:12px;padding:16px;}
    [data-testid="stMetricValue"], [data-testid="stMetricValue"] > div {
        font-size:clamp(1rem,1.6vw,1.65rem)!important;line-height:1.45;
        white-space:normal!important;overflow:visible!important;text-overflow:clip!important;
        overflow-wrap:anywhere;
    }
    [data-testid="stMetricLabel"] p {white-space:normal;overflow-wrap:anywhere;}
    [data-testid="stImage"] img {max-width:100%;height:auto;object-fit:contain;}
    .eyebrow {color:#ff4c56;letter-spacing:.16em;font-size:.78rem;font-weight:700;}
    .hero {border-left:4px solid #E50914;padding:8px 0 8px 20px;margin:12px 0 28px;}
    @media(max-width:640px){.block-container{padding:1rem;}h1{font-size:2rem!important;}}
    </style>''', unsafe_allow_html=True)
    try:
        results = load_results()
    except (OSError, ValueError, KeyError, IndexError) as exc:
        st.error('필수 결과 파일을 읽을 수 없습니다. dashboard/README.md의 파일 구성을 확인해 주세요.')
        st.caption(str(exc))
        st.stop()
    st.sidebar.markdown('**ABA3 · 1차 프로젝트**')
    st.sidebar.markdown('데이터 분석과 AI 브랜드 비주얼')
    st.sidebar.markdown('[01. Project Overview](#overview)\n\n[02. EDA](#eda)\n\n[03. Model Performance](#performance)\n\n[04. AI Creative Results](#creative)')
    st.sidebar.caption('저장된 결과를 읽는 대시보드입니다. 모델 학습·예측·AI 생성을 실행하지 않습니다.')
    st.markdown('<div class="eyebrow">ABA3 / DATA × AI CREATIVE</div>', unsafe_allow_html=True)
    st.title('Netflix TOP 10\n흥행 지속성과 AI 브랜드 비주얼')
    st.markdown('<div class="hero">첫 관측의 데이터에서, 작품별 비주얼 콘셉트까지.<br>데이터 분석 → 흥행 지속성 예측 → 공식 정보 검증 → AI 비주얼 제작</div>', unsafe_allow_html=True)

    st.header('01. Project Overview', anchor='overview')
    st.write('첫 관측 주의 TOP 10 순위·시청 시간·카테고리로 이후 두 달력 주의 글로벌 TOP 10 추가 등장 횟수를 예측할 수 있을까요?')
    st.info('예측 대상은 첫 관측 주 t를 제외한 t+7일·t+14일의 추가 등장 횟수(0·1·2회)입니다. 첫 관측 주를 실제 최초 공개·진입 시점으로 단정하지 않습니다.')
    for col, label, value in zip(st.columns(4), ['수업 데이터','최종 분석 표본','학습/검증/평가','관측 기간'], ['29주','357개','251 / 60 / 46','2021.07–2022.01']):
        col.metric(label,value)
    st.caption('원본 데이터: 1,160행 · 관측 기간: 2021-07-04 ~ 2022-01-16 · 분석 단위: 작품·시즌 · 모델 재학습 없이 확정된 결과를 표시합니다.')

    st.header('02. EDA', anchor='eda')
    st.caption('관계 분석은 학습 데이터 251개만 사용했습니다.')
    st.image(str(ASSETS['eda']), caption='첫 관측 순위·시청 시간·카테고리와 이후 2주 추가 등장 횟수의 관계', use_container_width=True)
    ranks = results['ranks']
    high, low = ranks[ranks['weekly_rank'] <= 3], ranks[ranks['weekly_rank'] >= 8]
    a = float((high['n'] * high['mean']).sum() / high['n'].sum())
    b = float((low['n'] * low['mean']).sum() / low['n'].sum())
    st.write(f'학습 구간에서 첫 관측 순위 1–3위 집단의 실제 평균 추가 등장 횟수는 {a:.2f}회, 8–10위 집단은 {b:.2f}회였습니다. 상위 순위와 이후 등장 횟수 사이의 관련성을 보여주지만 인과관계는 아닙니다.')
    target_table = results['targets'].rename(columns={'target_2w':'실제 추가 등장 횟수(회)','n':'표본 수(개)'})
    st.dataframe(target_table, hide_index=True, use_container_width=True)
    st.caption('주간 시청 시간의 규모와 카테고리별 차이를 함께 고려합니다. 관측 구간 절단과 작품명 기반 식별의 한계가 있습니다.')

    st.header('03. Model Performance', anchor='performance')
    st.caption('동일한 검증 데이터 60개 · MAE는 낮을수록 좋으며 단위는 추가 등장 횟수(회)입니다.')
    val, log, test = results['val'], results['log'], results['test']
    values = [float(val['baseline_mae']), float(val['ridge_mae']), float(log['log1p_hours_mae'])]
    names = ['중앙값 기준선','기존 Ridge','개선 log1p Ridge']
    for col, name, score in zip(st.columns(3), names, values):
        col.metric(name, f'{score:.6f}')
    frame = pd.DataFrame({'모델':names,'검증 MAE(회)':values})
    chart = alt.Chart(frame).mark_bar(cornerRadiusEnd=5).encode(
        x=alt.X('검증 MAE(회):Q',scale=alt.Scale(domain=[0,0.8])),
        y=alt.Y('모델:N',sort=names,title=None),
        color=alt.Color('모델:N',scale=alt.Scale(domain=names,range=['#62626F','#A4A4AF','#E50914']),legend=None),
        tooltip=['모델',alt.Tooltip('검증 MAE(회):Q',format='.6f')]).properties(height=180,title='검증 MAE 비교 · 60개')
    st.altair_chart(chart,use_container_width=True)
    st.write(f"개선 log1p Ridge는 기존 Ridge의 시청 시간 입력에 log1p 변환을 적용한 모델입니다. 이 검증 구간에서 MAE는 {(values[1]-values[2])/values[1]*100:.2f}% 감소했습니다.")
    with st.container(border=True):
        st.markdown('**독립 평가 범위**')
        st.write(f"기존 Ridge 독립 평가 MAE: **{float(test['ridge_mae']):.6f}회** · 기존 평가 표본 46개")
        st.write('개선 log1p Ridge 독립 평가: **미실시**')
        st.caption('위 기존 test MAE는 개선 모델 성능이 아닙니다. 이미 분석된 test 46개를 새로운 독립 평가로 사용하지 않습니다.')
    st.image(str(ASSETS['insights']), caption='개선 모델 검증 60개: 예측값과 실제 결과, 예측 수준별 집단 비교', use_container_width=True)
    group_table = results['groups'][['group','n','mean_prediction','mean_actual']].copy()
    group_table['group'] = group_table['group'].map({'low':'낮음','middle':'중간','high':'높음'})
    group_table.columns = ['예측 수준','표본 수(개)','평균 예측(회)','실제 평균(회)']
    st.dataframe(group_table,hide_index=True,use_container_width=True)
    st.caption('예측값 순서로 나눈 세 집단은 각 20개입니다. 실제 평균은 낮음 0.25회 → 중간 0.70회 → 높음 1.60회였습니다. 검증 사례의 관찰 결과이며 인과관계나 마케팅 효과를 의미하지 않습니다.')

    st.header('04. AI Creative Results', anchor='creative')
    st.write('검증 예측값 기준 TOP 3를 선정했습니다. 동점은 공동 순위로 표시하며, 예측값은 국가별 순위나 통합 인기 점수가 아닙니다.')
    candidates = results['top3']
    table = pd.DataFrame([{'순위':'공동 1위' if r['prediction_rank']==1 else '3위',
                           '작품·시즌':r['show_title'] + (' · 시즌 1' if r['show_title']=='Hellbound' else ' · 시즌 2' if r['show_title']=='The Queen of Flow' else ''),
                           '향후 2주 예측(회)':f"{r['predicted_additional_weeks']:.6f}",
                           '비주얼 제작':'완료' if r['visual_status']=='created' else '공식 정보 미검증 · 보류'} for r in candidates])
    st.dataframe(table,hide_index=True,use_container_width=True)
    st.caption('실제 추가 등장 횟수·예측 오차는 후보 선정 기준으로 사용하지 않았습니다. 검증 데이터 기반 사례 연구이며 독립적인 미래 콘텐츠 예측 실험이 아닙니다.')
    left, right = st.columns(2)
    with left:
        st.subheader('Red Notice')
        st.image(str(ASSETS['red_notice']),caption='AI 생성 원본 보존 · 1024×1024 배포본',use_container_width=True)
        st.write('공식 소개의 미술품·불편한 협력·추적 단서를 바탕으로 제작했습니다. 붉은 표면과 골드 디테일은 AI의 창작 제안입니다.')
        st.markdown('[Netflix 공식 작품 페이지](https://www.netflix.com/title/81161626)')
    with right:
        st.subheader('Hellbound · 시즌 1 후보')
        st.image(str(ASSETS['hellbound']),caption='AI 생성 원본 보존 · 1024×1024 배포본',use_container_width=True)
        st.write('초자연적 존재·신성한 심판 단서에 기반한 창작입니다. 라벤더색 유리와 민트빛 선은 AI의 제안이며 공식 시각 정보가 아닙니다.')
        st.write('AI 자동 생성 결과는 라벤더색 유리 소재로 제작되었으나, 작품의 심판·공포 분위기를 전달하는 데 한계가 있었다.')
        st.caption('공식 소개는 시리즈 전체 범위입니다. 시즌 1 전용 줄거리의 재현으로 해석하지 않습니다.')
        st.markdown('[Netflix 공식 작품 페이지](https://www.netflix.com/title/81256675)')
    st.info('The Queen of Flow 시즌 2는 공식 정보 확인에 실패해 이미지 생성을 보류했습니다. 장르·줄거리·디자인 태그를 추측하지 않았습니다.')
    st.warning('두 이미지는 공식 Netflix 캠페인이나 공식 로고가 아닌, 학습 프로젝트의 비공식 AI 브랜드 비주얼 콘셉트입니다. 비주얼의 홍보 효과·성과는 측정하지 않았습니다.')
    with st.expander('사용 자료와 해석 범위'):
        st.write('수업 제공 29주 글로벌 데이터의 확정 분석 결과를 사용합니다. TOP 3 공개 요약에는 작품·시즌·공동 순위·예측값·제작 상태만 포함했습니다. 개별 예측·오차·태그 원본·CLI 로그·인증 정보는 앱에서 읽거나 공개하지 않습니다.')
        st.code('reports/tables/course-eda-2week-2026-10-15/\nreports/tables/course-baseline-ridge-2026-10-15/metrics.csv\nreports/tables/course-ridge-log1p-validation-2026-10-19/metrics.csv\nreports/tables/course-log1p-business-insights-2026-10-19/prediction_groups.csv\ndashboard/data/top3_summary.json\nreports/final/ai-logo-assets/',language=None)
    st.divider()
    st.caption('ABA3 · Netflix TOP 10 / Data Analysis & AI Brand Visual · 저장된 결과를 읽는 포트폴리오')

if __name__ == '__main__':
    main()
