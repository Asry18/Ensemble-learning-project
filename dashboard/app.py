import json, os, sys
from pathlib import Path
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import joblib, numpy as np, pandas as pd, plotly.graph_objects as go, streamlit as st
import styles as S
from styles import fm, fl, icon

ROOT = Path(__file__).resolve().parents[1]
CAT = ["Brand", "Model", "Gear", "Fuel Type", "Town"]
NUM = ["YOM", "Engine", "Mileage", "Leasing", "IsNew", "AC", "PS", "PM", "PW"]
NAMES = {"YOM": "Year of manufacture", "Engine": "Engine capacity", "Mileage": "Mileage", "Brand": "Brand", "Model": "Model",
         "Gear": "Transmission", "Fuel Type": "Fuel type", "Town": "Town", "AC": "Air conditioning", "PS": "Power steering",
         "PM": "Power mirrors", "PW": "Power windows", "Leasing": "Leasing", "IsNew": "Brand new"}

st.set_page_config(page_title="AutoValue Sri Lanka – Used Vehicle Prices", page_icon="🚗", layout="wide")
S.inject()


# ------------------------------------------------------------------ data
@st.cache_data
def load():
    r = ROOT / "results"
    df = pd.read_csv(ROOT / "dataset/processed/clean.csv")
    df["Brand"] = df["Brand"].str.title().replace({"Bmw": "BMW", "Mg": "MG", "Kia": "KIA"})
    return (df, pd.read_csv(r / "predictions.csv"), pd.read_csv(r / "feature_importance.csv"),
            json.load(open(r / "metrics.json")))


@st.cache_resource
def models():
    import tensorflow as tf
    from xgboost import XGBRegressor
    xgb = XGBRegressor(); xgb.load_model(ROOT / "models/xgboost.json")
    return (joblib.load(ROOT / "models/preprocessor.pkl"), joblib.load(ROOT / "models/random_forest.pkl"), xgb,
            tf.keras.models.load_model(ROOT / "models/ann.keras"))


df, pred, imp, M = load()
RAW = pd.read_csv(ROOT / "dataset/processed/clean.csv")  # original casing, needed by the trained encoder


# ------------------------------------------------------------------ helpers
def kpi(label, value, note, ico, tint, ink):
    return (f'<div class="kpi"><div class="kpi-top"><span>{label}</span><span class="kpi-ico" style="background:{tint};color:{ink}">'
            f'{icon(ico)}</span></div><div class="kpi-val">{value}</div><div class="kpi-note">{note}</div></div>')


def card_head(title, sub=""):
    st.markdown(f'<p class="card-title">{title}</p><p class="card-sub">{sub}</p>', unsafe_allow_html=True)


def seg(label, options, default, key):
    v = st.segmented_control(label, options, default=default, key=key, label_visibility="collapsed")
    return v or default


def line_chart(x, y, n, name="Median price"):
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines+markers", line=dict(color=S.PRIMARY, width=2.5, shape="spline", smoothing=.4),
                               marker=dict(size=7, color="#FFFFFF", line=dict(color=S.PRIMARY, width=2.5)),
                               fill="tozeroy", fillcolor="rgba(79,70,229,.08)", customdata=n,
                               hovertemplate="<b>%{x}</b><br>" + name + " LKR %{y:.2f}M<br>%{customdata} listings<extra></extra>"))
    fig.update_yaxes(tickprefix="", ticksuffix="M", rangemode="tozero")
    fig.update_xaxes(type="category", nticks=7)
    return S.style(fig, 280)


def bar_h(labels, values, text, colors, height):
    fig = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker=dict(color=colors, cornerradius=6), text=text,
                           textposition="outside", cliponaxis=False, textfont=dict(color=S.TEXT, size=12.5),
                           hovertemplate="%{y}: %{text}<extra></extra>"))
    fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color="#334155", size=13))
    fig.update_xaxes(visible=False, showgrid=False)
    fig.update_layout(bargap=.45)
    return S.style(fig, height)


# ------------------------------------------------------------------ navigation
PAGES = ["Overview", "Market Explorer", "Comparison & Insights", "Price Estimator"]
SUB = {"Overview": "A snapshot of the Sri Lankan used-vehicle market, built from real listings.",
       "Market Explorer": "Filter the market by brand, fuel, transmission and year to see how prices move.",
       "Comparison & Insights": "How the pricing models stack up, and which factors move prices the most.",
       "Price Estimator": "Describe a vehicle to get an estimated price range from the trained models."}
with st.sidebar:
    st.markdown(f'<div class="brand"><div class="brand-mark">{icon("M5 16V12l2-5h10l2 5v4M3 16h18M7 16v2M17 16v2", 18, "#fff", 2)}</div>'
                f'<div>AutoValue <small>Sri Lanka</small></div></div>', unsafe_allow_html=True)
    page = st.radio("Views", PAGES, label_visibility="collapsed")
    st.markdown('<div class="side-note"><b>About the data</b>Advertised asking prices from Sri Lankan used-vehicle listings. '
                'Prices are shown in LKR millions.</div>', unsafe_allow_html=True)

st.markdown(f'<span class="topchip"><i></i>{len(df):,} listings analysed</span>', unsafe_allow_html=True)
st.markdown(f'<div class="page-title">{page}</div><p class="page-sub">{SUB[page]}</p>', unsafe_allow_html=True)

# ================================================================== OVERVIEW
if page == "Overview":
    top = df.Brand.value_counts()
    cols = st.columns(4, gap="medium")
    cards = [("Total listings", f"{len(df):,}", f"{df.Brand.nunique()} brands represented", "M4 6h16M4 12h16M4 18h10", S.PRIMARY_SOFT, S.PRIMARY),
             ("Median asking price", fm(df.Price.median()), "Half of listings are priced below this", "M12 2v20m5-16.5C16 4 14 3 12 3S7.5 4.2 7.5 6.5 9.5 9.5 12 10s4.5 1.5 4.5 3.5S14.5 17 12 17s-4-1-5-2.5", S.TEAL_SOFT, "#0F766E"),
             ("Automatic transmission", f"{(df.Gear == 'Automatic').mean():.0%}", "Share of all listings", "M12 15a3 3 0 100-6 3 3 0 000 6zm0-12v3m0 12v3M3 12h3m12 0h3", S.AMBER_SOFT, "#B45309"),
             ("Most listed brand", top.index[0], f"{top.iloc[0] / len(df):.0%} of all listings", "M5 16V12l2-5h10l2 5v4M3 16h18", S.PRIMARY_SOFT, S.PRIMARY)]
    for c, k in zip(cols, cards):
        c.markdown(kpi(*k), unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2, gap="medium")
    with a, st.container(border=True):
        card_head("Median price by year of manufacture", "Newer vehicles hold their value; each point is a year with 5+ listings")
        g = df[df.YOM >= 1995].groupby("YOM").Price.agg(["median", "count"]).query("count >= 5").reset_index()
        st.plotly_chart(line_chart(g.YOM.astype(str), g["median"] / 10, g["count"]), width="stretch", config={"displayModeBar": False})
    with b, st.container(border=True):
        card_head("Most listed brands", "Number of listings, top 8 brands")
        t8 = top.head(8)
        st.plotly_chart(bar_h(t8.index, t8.values, [f"{v:,}" for v in t8.values], [S.PRIMARY] * 8, 280), width="stretch", config={"displayModeBar": False})
    st.write("")
    with st.expander("Dataset preview", expanded=False):
        show = df.sample(10, random_state=7)[["Brand", "Model", "YOM", "Engine", "Gear", "Fuel Type", "Mileage", "Price"]].copy()
        show["Price"] = (show.Price / 10).map(lambda v: f"LKR {v:.2f}M")
        show["Mileage"] = show.Mileage.map(lambda v: f"{int(v):,} km"); show["Engine"] = show.Engine.map(lambda v: f"{int(v)} cc")
        st.dataframe(show.rename(columns={"YOM": "Year", "Gear": "Transmission", "Fuel Type": "Fuel"}), hide_index=True, width="stretch")
    st.caption("Mileage is almost perfectly (inversely) correlated with year of manufacture in this dataset (r ≈ −1.0, ~60 distinct values), so it behaves like a derived field rather than an independent odometer reading.")

# ================================================================== MARKET EXPLORER
elif page == "Market Explorer":
    with st.container(border=True):
        f1, f2, f3, f4 = st.columns([1, 1, 1, 1.5], gap="medium")
        brand = f1.selectbox("Brand", ["All brands"] + sorted(df.Brand.unique()))
        fuel = f2.selectbox("Fuel type", ["All fuel types"] + sorted(df["Fuel Type"].unique()))
        gear = f3.selectbox("Transmission", ["All"] + sorted(df.Gear.unique()))
        y0, y1 = f4.slider("Manufacture year", 1995, 2024, (1995, 2024))
        fl_ = df[(df.YOM >= y0) & (df.YOM <= y1)]
        if brand != "All brands": fl_ = fl_[fl_.Brand == brand]
        if fuel != "All fuel types": fl_ = fl_[fl_["Fuel Type"] == fuel]
        if gear != "All": fl_ = fl_[fl_.Gear == gear]
        med = fm(fl_.Price.median()) if len(fl_) else "–"
        iqr = f"{fm(fl_.Price.quantile(.25))} – {fm(fl_.Price.quantile(.75))}" if len(fl_) else "–"
        st.markdown(f'<span class="pill p">{len(fl_):,} listings</span><span class="pill n">Median {med}</span><span class="pill n">Middle 50%: {iqr}</span>', unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2, gap="medium")
    with a, st.container(border=True):
        card_head("Median price by year", "Years with 3+ listings in the current selection")
        g = fl_.groupby("YOM").Price.agg(["median", "count"]).query("count >= 3").reset_index()
        if len(g) < 2: st.info("Not enough listings for this selection.")
        else: st.plotly_chart(line_chart(g.YOM.astype(str), g["median"] / 10, g["count"]), width="stretch", config={"displayModeBar": False})
    with b, st.container(border=True):
        card_head("Price distribution", "Listings per price band; the top 5% of prices are excluded for readability")
        if len(fl_) < 10: st.info("Not enough listings for this selection.")
        else:
            cap = fl_.Price.quantile(.95); cnt, edges = np.histogram(fl_.Price[fl_.Price <= cap] / 10, bins=12)
            lab = [f"LKR {edges[i]:.1f}M – {edges[i + 1]:.1f}M" for i in range(12)]
            fig = go.Figure(go.Bar(x=lab, y=cnt, marker=dict(color=S.PRIMARY, cornerradius=6), customdata=(cnt / len(fl_) * 100).round(1),
                                   hovertemplate="<b>%{x}</b><br>%{y} listings<br>%{customdata}% of selection<extra></extra>"))
            fig.update_xaxes(tickmode="array", tickvals=[lab[i] for i in (0, 3, 6, 9, 11)], ticktext=[f"{edges[i]:.1f}M" for i in (0, 3, 6, 9, 11)])
            fig.update_layout(bargap=.12)
            st.plotly_chart(S.style(fig, 280), width="stretch", config={"displayModeBar": False})

# ================================================================== COMPARISON & INSIGHTS
elif page == "Comparison & Insights":
    T = M["test"]; xg = T["XGBoost"]
    c1, c2 = st.columns([1, 3])
    c1.markdown('<p class="lbl" style="margin-top:12px;font-size:14px">Compare XGBoost with</p>', unsafe_allow_html=True)
    with c2: other_name = seg("Compare with", ["Random Forest", "ANN", "Hybrid RF+ANN"], "Random Forest", "cmp")
    ot = T[other_name]; mx = max(xg["MAE"], ot["MAE"]); xg_best = xg["MAE"] <= ot["MAE"]

    def mcard(name, m, color, tint, ink, best):
        badge = f'<span class="badge" style="background:{tint};color:{ink};{"" if best else "visibility:hidden"}">Lower error</span>'
        return (f'<div class="mcard"><div class="mhead"><span><span class="mdot" style="background:{color}"></span>{name}</span>{badge}</div>'
                f'<div class="mlabel" style="margin-top:20px">Typical error (MAE)</div><div class="mbig">{fl(m["MAE"])}</div>'
                f'<div class="track"><div style="width:{m["MAE"] / mx * 100:.1f}%;background:{color}"></div></div>'
                f'<div class="msub"><div><span class="mlabel">RMSE</span><b>{fl(m["RMSE"])}</b></div><div><span class="mlabel">R² (variance explained)</span><b>{m["R2"]:.3f}</b></div></div></div>')
    a, b = st.columns(2, gap="medium")
    a.markdown(mcard("XGBoost", xg, S.TEAL, S.TEAL_SOFT, "#0F766E", xg_best), unsafe_allow_html=True)
    b.markdown(mcard(other_name, ot, S.AMBER, S.AMBER_SOFT, "#92400E", not xg_best), unsafe_allow_html=True)
    rel = abs(xg["MAE"] - ot["MAE"]) / mx * 100
    txt = f'{"XGBoost" if xg_best else other_name} has the lower typical error, by {rel:.0f}% (MAE) on the held-out test set.'
    if other_name == "Random Forest" and "bootstrap_rf_vs_xgb" in M:
        bt = M["bootstrap_rf_vs_xgb"]["MAE"]
        txt += f' Resampling the test set puts the gap at about {fl(bt["mean_diff_RF_minus_XGB"])} (95% interval {fl(bt["ci95"][0])} to {fl(bt["ci95"][1])}), so the difference is unlikely to be noise.'
    if other_name == "Hybrid RF+ANN":
        w = M["hybrid_rf_weight"]; txt += f" The hybrid blends {w:.0%} Random Forest with {1 - w:.0%} ANN, and did not beat its strongest component."
    st.write("")
    st.markdown(f'<div class="insight"><div class="ico">{icon("M9 18h6M10 21h4M12 3a6 6 0 00-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0012 3z", 18, sw=2)}</div><div><b style="color:{S.TEXT}">Insight.</b> {txt}</div></div>', unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        h1, h2 = st.columns([3, 1.4])
        with h1: card_head("What drives vehicle prices", "Relative importance of each factor (one-hot columns summed per factor)")
        with h2: which = seg("Importance model", ["XGBoost", "Random Forest"], "XGBoost", "imp")
        d = imp.assign(feature=imp.feature.map(lambda f: NAMES.get(f, f))).sort_values(which, ascending=False).head(9)
        cols = [S.PRIMARY] + ["#A5B4FC"] * (len(d) - 1)
        st.plotly_chart(bar_h(d.feature, d[which], [f"{v * 100:.1f}%" for v in d[which]], cols, 360), width="stretch", config={"displayModeBar": False})
    st.write("")
    with st.container(border=True):
        h1, h2 = st.columns([3, 2])
        with h1: card_head("Actual vs predicted", "Held-out test listings under LKR 15M; the dashed line is a perfect prediction")
        with h2: pm = seg("Model", ["XGBoost", "Random Forest", "ANN", "Hybrid RF+ANN"], "XGBoost", "avp")
        d = pred[pred.actual < 150]
        fig = go.Figure(go.Scatter(x=d.actual / 10, y=d[pm] / 10, mode="markers", marker=dict(size=6, color=S.TEAL if pm == "XGBoost" else S.PRIMARY, opacity=.45),
                                   hovertemplate="Actual LKR %{x:.2f}M<br>Predicted LKR %{y:.2f}M<extra></extra>"))
        fig.add_shape(type="line", x0=0, y0=0, x1=15, y1=15, line=dict(color="#94A3B8", dash="dash", width=1.5))
        fig.update_xaxes(ticksuffix="M", title="Actual price"); fig.update_yaxes(ticksuffix="M", title="Predicted price")
        st.plotly_chart(S.style(fig, 340), width="stretch", config={"displayModeBar": False})

# ================================================================== PRICE ESTIMATOR
else:
    pre, rf, xgb, ann = models()
    brands = sorted(RAW.Brand.unique())
    left, right = st.columns([1.15, 1], gap="large")
    with left:
        with st.container(border=True):
            card_head("Vehicle details")
            c1, c2 = st.columns(2)
            brand = c1.selectbox("Brand", brands, index=brands.index("TOYOTA"), format_func=str.title)
            mods = RAW[RAW.Brand == brand].Model.value_counts().index.tolist()
            model = c2.selectbox("Model", mods)
            sub = RAW[(RAW.Brand == brand) & (RAW.Model == model)]
            year = st.slider("Year of manufacture", 1980, 2024, int(sub.YOM.median()))
        with st.container(border=True):
            card_head("Specifications")
            c1, c2 = st.columns(2)
            eng = c1.number_input("Engine capacity (cc)", 500, 6000, int(sub.Engine.median()), step=50)
            fit = np.polyfit(RAW.YOM, RAW.Mileage, 1)
            mil = c2.number_input("Mileage (km)", 0, 900000, int(round(max(0, np.polyval(fit, year)), -3)), step=5000, key=f"mil_{year}")
            c1, c2 = st.columns(2)
            c1.markdown('<p class="lbl">Transmission</p>', unsafe_allow_html=True)
            with c1: gear = seg("Transmission", ["Automatic", "Manual"], "Automatic", "gear")
            fuel = c2.selectbox("Fuel type", ["Petrol", "Diesel", "Hybrid", "Electric"])
        with st.container(border=True):
            card_head("Features and condition")
            t1, t2 = st.columns(2)
            ac = t1.toggle("Air conditioning", True); ps = t2.toggle("Power steering", True)
            pm_ = t1.toggle("Power mirrors", True); pw = t2.toggle("Power windows", True)
            new = t1.toggle("Brand new", False); lease = t2.toggle("Ongoing lease", False)
        b1, b2 = st.columns([3, 1])
        go_btn = b1.button("Estimate price", type="primary", width="stretch")
        reset = b2.button("Reset", width="stretch")

    form = dict(Brand=brand, Model=model, Gear=gear, **{"Fuel Type": fuel}, Town="Colombo", YOM=year, Engine=eng, Mileage=mil,
                Leasing=int(lease), IsNew=int(new), AC=int(ac), PS=int(ps), PM=int(pm_), PW=int(pw))
    if reset:
        st.session_state.pop("committed", None); st.rerun()
    if go_btn or "committed" not in st.session_state:
        st.session_state["committed"] = form
    f = st.session_state["committed"]

    A = pre.transform(pd.DataFrame([f])[CAT + NUM])
    px_ = {"XGBoost": float(xgb.predict(A)[0]), "Random Forest": float(rf.predict(A)[0]), "ANN": float(ann.predict(A, verbose=0)[0, 0])}
    px_["Hybrid RF+ANN"] = M["hybrid_rf_weight"] * px_["Random Forest"] + (1 - M["hybrid_rf_weight"]) * px_["ANN"]
    P = {k: float(np.expm1(v)) for k, v in px_.items()}
    est = P["XGBoost"]                                           # best model on the test set
    trees = np.expm1(np.array([t.predict(A.astype(np.float32))[0] for t in rf.estimators_]))
    lo, hi = float(min(np.percentile(trees, 10), est)), float(max(np.percentile(trees, 90), est))
    comp = df[(df.Brand == f["Brand"].title()) & ((df.YOM - f["YOM"]).abs() <= 1)].Price
    mkt = float(comp.median()) if len(comp) >= 5 else float(df[df.Brand == f["Brand"].title()].Price.median())
    spread = (hi - lo) / est
    conf = ("Tight range", S.TEAL_SOFT, "#0F766E") if spread < .25 else ("Moderate range", S.AMBER_SOFT, "#92400E") if spread < .55 else ("Wide range", "#FEE2E2", "#991B1B")
    dom_lo, dom_hi = min(lo, mkt) * .8, max(hi, mkt) * 1.15
    pc = lambda v: (v - dom_lo) / (dom_hi - dom_lo) * 100
    dm = (est - mkt) / mkt * 100
    agree = (max(P.values()) - min(P.values())) / np.mean(list(P.values())) * 100
    tk = [(f'Estimated with XGBoost, the most accurate model on held-out data, for a {f["YOM"]} {f["Brand"].title()} {f["Model"]}.', S.PRIMARY_SOFT, S.PRIMARY),
          (f'This is {"in line with" if abs(dm) < 3 else f"{abs(dm):.0f}% " + ("above" if dm > 0 else "below")} the typical {f["Brand"].title()} listed within a year of {f["YOM"]} ({fm(mkt)}).', S.AMBER_SOFT, "#92400E"),
          (f'The four models agree within {agree:.0f}% of each other.' + (" Check condition and trim before relying on a wide range." if spread >= .55 else ""), conf[1], conf[2])]
    take_html = "".join(f'<div class="take"><i style="background:{t};color:{k}">✓</i><span>{x}</span></div>' for x, t, k in tk)
    mini = "".join(f'<div>{k}<b>{fm(v)}</b></div>' for k, v in P.items())
    with right:
        st.markdown(f"""<div class="sticky-marker"></div><div class="result">
          <div class="res-top"><span class="res-eyebrow">Estimated price</span><span class="badge" style="background:{conf[1]};color:{conf[2]}">{conf[0]}</span></div>
          <div class="res-price">{fm(est)}</div>
          <div class="res-range">Likely range <b>{fm(lo)} – {fm(hi)}</b></div>
          <div class="rbar"><div class="base"></div><div class="span" style="left:{pc(lo):.1f}%;width:{pc(hi) - pc(lo):.1f}%"></div>
            <div class="mid" style="left:{pc(est):.1f}%"></div><div class="mkt" style="left:{pc(mkt):.1f}%"></div></div>
          <div class="legend"><span><i style="width:14px;height:8px;border-radius:4px;background:{S.PRIMARY};display:inline-block"></i>Likely range</span>
            <span><i style="width:4px;height:14px;border-radius:2px;background:{S.TEXT};display:inline-block"></i>Estimate</span>
            <span><i style="width:12px;height:12px;border-radius:50%;background:{S.AMBER};box-shadow:0 0 0 1px #D97706;display:inline-block"></i>Brand typical ({f["YOM"]})</span></div>
          <div class="res-h">Key takeaways</div>{take_html}
          <div class="res-h" style="margin-top:6px">All models</div><div class="mini">{mini}</div>
          <p class="fine">Range is the middle 80% of the Random Forest's individual trees. Predictions are for advertised asking prices, not final sale prices.</p>
        </div>""", unsafe_allow_html=True)
