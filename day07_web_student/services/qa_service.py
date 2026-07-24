from pathlib import Path

import pandas as pd


def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    normalized = question.replace(" ", "").lower()

    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有{int(metrics['用户数']):,}名用户。"
    # TODO 4-1：补充“流失率”“偏好品类”“生命周期风险”和“订单”四类问答。
    # 每个回答都必须引用data目录中已经计算的指标，不得编造数值。
    if "流失率" in normalized or "流失" in normalized:
        return f"当前整体流失率为{metrics['流失率']:.1%}，流失用户共{int(metrics['流失人数']):,}人。"
    if "品类" in normalized or "偏好" in normalized or "类别" in normalized:
        top_cat = category_df.loc[category_df["用户数"].idxmax()]
        return (
            f"用户最偏好的品类是【{top_cat['PreferedOrderCat']}】，"
            f"共有{int(top_cat['用户数']):,}人，占比约{top_cat['用户占比']:.1%}。"
        )
    if "生命" in normalized or "周期" in normalized or "风险" in normalized or "阶段" in normalized:
        max_churn = segment_df.loc[segment_df["流失率"].idxmax()]
        return (
            f"流失风险最高的生命周期阶段是【{max_churn['TenureGroup']}】，"
            f"流失率达{max_churn['流失率']:.1%}，涉及{int(max_churn['用户数']):,}名用户。"
        )
    if "订单" in normalized or "下单" in normalized:
        return (
            f"用户平均订单数为{metrics['平均订单数']:.2f}单，"
            f"订单数中位数为{int(metrics['订单数中位数'])}单。"
        )

    return (
        "抱歉，我暂时无法回答这个问题。请尝试询问：总用户数、流失率、偏好品类、生命周期风险或订单情况。"
        "请换一种更具体的问法。"
    )
