# -*- coding: utf-8 -*-
"""
『男性性女性性の幸せバランス診断』 (joy_checker_app-v5.py)

「ひとり恋愛メソッド」および講義動画の深層論理を反映し、
今日あった嬉しかった出来事から「男性性」と「女性性」のエネルギー、
および内なる「セルフパートナーシップ（自分彼氏×自分彼女）」の状態を精密に診断するアプリ。

【v5の進化ポイント】
- 9種類の詳細診断タイプ（純粋受容、五感解放、日常のトキメキ、目標達成、能動的提供、評価・客観価値獲得、セルフパートナーシップ統合、感謝共振循環、自己対話・育み型）
- 客観的評価/思考（男性性）と、五感・体感・没頭（女性性）を識別する多重文脈解析
- 深層解説＋愛されアドバイス＋今日の実践アクションの3重出力
"""

import sys
import re

# ==========================================
# キーワード・パターン定義
# ==========================================
FEM_RECEIVE_PATTERNS = [
    r"もらった", r"された", r"奢して", r"ご馳走", r"プレゼント", r"ギフト", r"差し入れ",
    r"褒められ", r"カワイイ", r"可愛い", r"愛され", r"大切にされ", r"誘われ", r"受け入れ",
    r"手伝って", r"助けられ", r"庇われ", r"共感され", r"聴いてもらった", r"優しくされ", r"奢ってもらった"
]

FEM_SENSORY_PATTERNS = [
    r"美味しい", r"おいしい", r"気持ちよかっ", r"癒やされ", r"ほっとした", r"安心", r"リラックス",
    r"温泉", r"カフェ", r"マッサージ", r"甘え", r"味わう", r"まったり", r"共感", r"ぬくもり", r"幸せ",
    r"やさしく", r"抱きしめ", r"温かい", r"うっとり", r"トキメキ", r"ときめき", r"美しい", r"綺麗",
    r"キレイ", r"五感", r"感触", r"香り", r"音", r"空間", r"浸る", r"感動", r"景色", r"朝日", r"空",
    r"ゆるむ", r"緩んだ", r"じんわり", r"心地いい", r"心地よかった"
]

MASC_ACHIEVE_PATTERNS = [
    r"達成", r"成功", r"完成", r"クリア", r"合格", r"勝つ", r"勝った", r"契約", r"成果", r"解決",
    r"やり切っ", r"やり遂げ", r"納品", r"稼いだ", r"売り上げ", r"昇進", r"目標", r"克服", r"突破",
    r"決断", r"克服した", r"やり遂げた", r"やりきった"
]

MASC_ACTION_PATTERNS = [
    r"あげた", r"プレゼントした", r"奢った", r"助けた", r"解決した", r"導いた", r"作っ", r"作った",
    r"挑戦", r"自分で", r"購入した", r"買った", r"任され", r"頼られ", r"ランニング", r"撮影",
    r"企画", r"提案", r"行動", r"選択", r"移動", r"走っ", r"決めた"
]

MASC_EVAL_PATTERNS = [
    r"コスパ", r"安く", r"得した", r"お得", r"評価", r"価値", r"褒められた", r"認められた",
    r"ランク", r"効率", r"スムーズ", r"完璧", r"正解", r"役に立った"
]

GRATITUDE_PATTERNS = [
    r"ありがとう", r"感謝", r"有難い", r"おかげ", r"恩恵", r"神様", r"宇宙"
]


def analyze_joy(text: str) -> dict:
    """入力された文章を解析し、喜びのカテゴリー、比率、深層解説、アドバイスを出力する関数"""
    if not text or not text.strip():
        return {"error": "嬉しかった出来事を文章で入力してください。"}

    fem_rec_score = sum(len(re.findall(p, text)) for p in FEM_RECEIVE_PATTERNS)
    fem_sens_score = sum(len(re.findall(p, text)) for p in FEM_SENSORY_PATTERNS)
    masc_ach_score = sum(len(re.findall(p, text)) for p in MASC_ACHIEVE_PATTERNS)
    masc_act_score = sum(len(re.findall(p, text)) for p in MASC_ACTION_PATTERNS)
    masc_eval_score = sum(len(re.findall(p, text)) for p in MASC_EVAL_PATTERNS)
    gratitude_score = sum(len(re.findall(p, text)) for p in GRATITUDE_PATTERNS)

    # 構造的構文解析（文脈・思考と感性の補正）
    if re.search(r"(してもらった|してくれた|受け取った|くれた|ご馳走になった|奢ってもらった|褒められた)", text):
        fem_rec_score += 2.0
    if re.search(r"(してあげた|やってやった|達成できた|自分でできた|やり切った|自分で買った|決めた)", text):
        masc_act_score += 2.0
    if re.search(r"(味わった|うっとり|感動した|美しかった|気持ちよかった|癒やされた|ほっとした)", text):
        fem_sens_score += 2.0
    if re.search(r"(コスパ|お得|安く買えた|スムーズにできた|評価された|認められた)", text):
        masc_eval_score += 2.0

    total_fem = fem_rec_score + fem_sens_score
    total_masc = masc_ach_score + masc_act_score + masc_eval_score
    grand_total = total_fem + total_masc

    if grand_total == 0:
        ratio_fem = 50.0
        ratio_masc = 50.0
    else:
        ratio_fem = round((total_fem / grand_total) * 100, 1)
        ratio_masc = round((total_masc / grand_total) * 100, 1)

    # 全9パターンの精密診断ロジック
    if ratio_fem >= 65.0 and fem_rec_score >= fem_sens_score and fem_rec_score > 0:
        pattern_id = "fem_receive"
        title = "【女性性の喜び：純粋受容・愛され受け取り型】"
        summary = (
            "人や世界からの愛、好意、プレゼント、優しさを素直に「受け取る」ことで心が満たされた喜びです。\n"
            "「愛されること」「甘えること」に対して心をオープンに開き、自分自身に『受け取る許可』が出せている素晴らしい状態です。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "あなたは素晴らしい「受け取り上手（自分彼女の開花）」の才能を発揮しています！\n"
            "「お返しをしなきゃ」「申し訳ない」という思考を手放し、「私は大切にされて当然♡」と純粋に受け取り切りましょう。\n"
            "弾けるような「嬉しい！」「ありがとう！」という感謝の笑顔を表現すると、周りの男性性（パートナーや環境）がさらにあなたを喜ばせようと動き出します。"
        )
        action_step = "💡 今日のアクション: 「嬉しい♡ありがとう！」の気持ちを、素直な言葉や笑顔で相手や周りの環境に伝えてみましょう。"

    elif ratio_fem >= 60.0 and fem_sens_score > fem_rec_score:
        pattern_id = "fem_sensory"
        title = "【女性性の喜び：五感・身体感覚・感性解放型】"
        summary = (
            "頭の思考（評価・損得・損得勘定）を静め、五感や身体感覚で「いまここ」の快・心地よさ・美しさに全身で没頭できた喜びです。\n"
            "身体の感覚が開いており、内なる「自分彼女」が温かい充足感と快感で満たされている理想的な状態です。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "損得や正しさではなく、「身体がどう感じているか（うっとりする、ほっとする、胸が高鳴る）」を大切にできています。\n"
            "この五感の感性こそが、あなたの女性性のエネルギーの源泉です。\n"
            "五感で味わった心地よさや感動の余韻をじっくり身体に染み込ませることで、直感力と引き寄せ力が飛躍的に高まります。"
        )
        action_step = "💡 今日のアクション: その心地よかった感触、味わい、香りを目を閉じて思い出し、身体全体で3秒間深く浸ってみましょう。"

    elif ratio_fem >= 55.0 and fem_sens_score > 0 and (fem_rec_score == 0 and masc_eval_score == 0):
        pattern_id = "fem_subtle"
        title = "【女性性の喜び：日常の微細なトキメキ・安心浸り型】"
        summary = (
            "大きな成果や特別な刺激に頼らず、日常の些細な一瞬（ほっとするお茶の時間、美しい空、ぬくもり）に幸せを見出せた穏やかで深い喜びです。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "あなたの感性の感度がとても豊かに開いています。\n"
            "「何でもない日常」の中に小さなトキメキを感じられるのは、自分を愛する基礎の土台（安心感）が整っている証拠です。\n"
            "この小さな「幸せのカウント」を積み重ねることで、あなたの波動のベースラインが底上げされ、自然体で愛される体質になります。"
        )
        action_step = "💡 今日のアクション: 今日感じた小さな「ほっとした瞬間」や「綺麗だなと思った景色」をノートや写真に残してみましょう。"

    elif ratio_masc >= 65.0 and masc_ach_score >= masc_act_score and masc_ach_score > 0:
        pattern_id = "masc_achieve"
        title = "【男性性の喜び：目標達成・自己突破・成果実現型】"
        summary = (
            "自らの意志と集中力を結集し、難題や目標を力強くクリアした「自己効力感と突破力」の喜びです。\n"
            "内なる「自分彼氏」の行動力がしっかりと現実を動かし、具体的な成果を生み出せた瞬間です。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "あなたの中の頼もしい「行動力・実現力（自分彼氏）」が見事に発揮されました！\n"
            "達成した直後にすぐ「次はどうしよう」と焦るのではなく、「自分、本当によく頑張った！」と自分の奮闘と成果をしっかり認め、称えてあげてください。\n"
            "自分彼氏を褒めて労うことで、内なる信頼関係（セルフパートナーシップ）がより強固になります。"
        )
        action_step = "💡 今日のアクション: 自分の胸に手を当てて「よくやったね、最高の成果だよ！」と自分自身をたっぷり褒めてあげましょう。"

    elif ratio_masc >= 60.0 and masc_act_score > masc_ach_score and masc_eval_score == 0:
        pattern_id = "masc_action"
        title = "【男性性の喜び：能動的行動・リード・価値提供型】"
        summary = (
            "自らが主体となって決断・行動を起こし、誰かに価値を提供したり、新しい選択を切り拓いた喜びです。\n"
            "「自分の力で選択し、与え、創造する」という頼もしい能動的パワーが存分に回っています。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "周囲や自分自身に対して「与える力」「導く力」が力強く働いています。\n"
            "あなたが起点となって動いたことで、周囲に安心や歓びの波紋が広がっています。\n"
            "自ら動いて価値を生み出せる自分への信頼（自己信頼感）を深めつつ、頑張った自分を最後はゆったり休ませてあげましょう。"
        )
        action_step = "💡 今日のアクション: 自分が起こした行動や決断によって生まれたポジティブな変化を紙やノートに書き留めてみましょう。"

    elif ratio_masc >= 60.0 and masc_eval_score > 0:
        pattern_id = "masc_eval"
        title = "【男性性の喜び：評価承認・客観価値獲得型】"
        summary = (
            "コスパ、効率、周囲からの評価や認められた実感など、「客観的な価値や正解」を得られたことで手応えを感じた喜びです。\n"
            "頭の思考や判断力（男性性）が鋭く働き、スマートに物事をコントロールできた状態です。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "思考力と客観的な判断力が見事に成果を結びつけました！\n"
            "頭で「得した」「評価された」という満足感を得たあとは、「それで、私の心や身体はどんな気持ち？」と内なる女性性（感覚）に優しく問いかけてみましょう。\n"
            "思考の満足と感情の心地よさの両方を満たすことで、満足感がより深く持続します。"
        )
        action_step = "💡 今日のアクション: 「頭で得したこと」だけでなく、「身体が感じた心地よさ」を1つ探してノートに書いてみましょう。"

    elif gratitude_score > 0 and (40.0 <= ratio_fem <= 60.0):
        pattern_id = "gratitude_cycle"
        title = "【高次元循環：感謝・愛の共振循環型】"
        summary = (
            "単なる出来事の損得を超えて、人や環境、目に見えない配慮や恩恵に対する「温かい感謝の波動」が溢れ出た喜びです。\n"
            "男性性の行動と女性性の受容が「感謝」という最高次元の波動で結ばれています。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "心からの感謝が湧き出ている状態は、あらゆる引き寄せの中で最も高いエネルギー状態です！\n"
            "その温かい感謝の気持ちを、言葉や笑顔、温かい態度で外の世界へ循環させましょう。\n"
            "外に出された感謝のエネルギーは倍になってあなたのもとへ舞い戻り、さらなる奇跡的な愛と豊かさを引き寄せます。"
        )
        action_step = "💡 今日のアクション: 感謝したい人や出来事に向けて、心の中で「ありがとう」と念じるか、直接メッセージを送ってみましょう。"

    elif 40.0 <= ratio_fem <= 60.0:
        pattern_id = "integration"
        title = "【女性性と男性性の統合：内なるセルフパートナーシップ相思相愛型】"
        summary = (
            "自ら能動的に意志を持って行動・選択した男性性のパワー（自分彼氏）と、そのプロセスや成果を五感で素直に受け取り味わった女性性の感性（自分彼女）が見事に協奏した喜びです。\n"
            "内なる「行動する自分」と「感じる自分」が完璧な相思相愛（両思い）で巡っています。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "「与える力・動く力（男性性）」と「受け取る力・感じる力（女性性）」が理想的な黄金バランスで循環しています！\n"
            "自分を最高のスポットに連れて行ってくれた「自分彼氏」の行動力を称え、そこで得られた感動を「自分彼女」として全身で味わうという最高のセルフパートナーシップが完成しています。\n"
            "この内なる調和状態を維持することで、現実のパートナーシップでも理想的な愛と好意を自然体で引き寄せ続けます。"
        )
        action_step = "💡 今日のアクション: 「自分を最高の場所に連れて行ってくれてありがとう♡」「この感動を味わえて幸せ！」と内なる対話をしてみましょう。"

    else:
        pattern_id = "self_dialogue"
        title = "【調整・自己対話型：内なるパートナーシップ育み型】"
        summary = (
            "日常の中での小さな気づきや、自分への労い・受け入れの第一歩が踏み出せた穏やかな芽生えの喜びです。\n"
            "ネガティブな感情や迷いも含めて「今の自分」をそのまま受け容れようとしている優しい段階です。"
        )
        advice = (
            "【愛され力を高めるアドバイス】\n"
            "自分の心と身体の声に耳を傾けようとする、温かい自己愛の意識が育っています。\n"
            "「こうあるべき」という理想に自分を当てはめる必要はありません。\n"
            "「どんな自分でも味方でいるよ」と内なる自分に声をかけてあげることで、安心感が深まり、女性性のエネルギーがのびのびと開花していきます。"
        )
        action_step = "💡 今日のアクション: 温かい飲み物を飲みながら、「今日も1日よく頑張ったね」と自分に優しく声をかけてあげましょう。"

    return {
        "input_text": text,
        "pattern_id": pattern_id,
        "category": title,
        "ratio_fem": ratio_fem,
        "ratio_masc": ratio_masc,
        "summary": summary,
        "advice": advice,
        "action_step": action_step
    }


def cli_run():
    print("=" * 60)
    print("      ✨ 男性性女性性の幸せバランス診断 (v5) ✨")
    print("  〜 今日あった嬉しかったことから内なるエネルギーを判定 〜")
    print("=" * 60)
    
    test_input = "今朝、ランニングに行って朝日の写真を撮ったら、神様が降りてきてるみたいな超絶美しい写真が撮れて感動した"
    print(f"■ 入力例: {test_input}\n")
    res = analyze_joy(test_input)
    print(f"★ 判定結果: {res['category']}")
    print(f"   ・女性性の喜び度 : {res['ratio_fem']}%")
    print(f"   ・男性性の喜び度 : {res['ratio_masc']}%")
    print("-" * 60)
    print(f"■ 喜びの深層解説:\n{res['summary']}\n")
    print(f"■ 愛され力を高めるアドバイス:\n{res['advice']}\n")
    print(f"{res['action_step']}")
    print("=" * 60 + "\n")


# ==========================================
# Streamlit Web UI サポート
# ==========================================
def main_streamlit():
    import streamlit as st

    st.set_page_config(
        page_title="男性性女性性の幸せバランス診断",
        page_icon="✨",
        layout="centered"
    )

    st.markdown(
        """
        <style>
        .stApp {
            background-color: #fffafc;
        }
        .main-title {
            text-align: center;
            color: #d81b60;
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .sub-title {
            text-align: center;
            color: #880e4f;
            font-size: 14px;
            margin-bottom: 25px;
        }
        .result-card {
            background: linear-gradient(135deg, #fff0f5 0%, #ffffff 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #f8bbd0;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .badge-title {
            color: #c2185b;
            font-size: 18px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">✨ 男性性女性性の幸せバランス診断 ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">〜 今日あった嬉しかったことから、あなたのあなたの「男性性」と「女性性」の循環を紐解く 〜</div>', unsafe_allow_html=True)

    st.write("今日あった「嬉しかったこと」「楽しかったこと」を自由に入力してください♡")
    
    st.write("👨男性性は行動する力、挑戦する力、考える力、カタチにする力")
    st.write("👩女性性は感じる力、創造する力、共鳴する力、引き寄せる力")

    # 入力例ボタン
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    default_val = ""
    if col_ex1.button("🍰 ケーキをもらった"):
        default_val = "今日は同僚に仕事を手伝ってもらって、美味しいケーキをご馳走になった！"
    if col_ex2.button("🌅 朝日に感動した"):
        default_val = "今朝、ランニングに行って朝日の写真を撮ったら、神様が降りてきてるみたいな超絶美しい写真が撮れて感動した"
    if col_ex3.button("🎯 目標を達成した"):
        default_val = "今月難しかったプロジェクトの目標数字を自力で達成して褒められた！"

    user_input = st.text_area("▼ 今日の出来事を入力", value=default_val, height=100, placeholder="例: 欲しかった服を試着したらサイズもピッタリでワクワクした！")

    if st.button("💖 喜びのバランスを診断する", use_container_width=True):
        if not user_input.strip():
            st.warning("嬉しかった出来事を文章で入力してください。")
        else:
            res = analyze_joy(user_input)

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="badge-title">判定結果: {res["category"]}</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            col1.metric("👩 女性性の喜び度", f"{res['ratio_fem']}%")
            col2.metric("👨 男性性の喜び度", f"{res['ratio_masc']}%")

            st.progress(res['ratio_fem'] / 100.0)

            st.markdown("### 📖 喜びの深層解説")
            st.write(res["summary"])

            st.markdown("### 💖 愛され力を高めるアドバイス")
            st.info(res["advice"])

            st.success(res["action_step"])
            st.markdown('</div>', unsafe_allow_html=True)

            # LINE/SNSシェア用テキスト枠
            st.markdown("### 📱 LINE・SNSシェア用テキスト")
            share_text = (
                f"【男性性女性性の幸せバランス診断結果】\n"
                f"出来事: 「{user_input}」\n\n"
                f"★ 判定: {res['category']}\n"
                f"・女性性: {res['ratio_fem']}%\n"
                f"・男性性: {res['ratio_masc']}%\n\n"
                f"【アドバイス】\n{res['advice']}\n\n"
                f"{res['action_step']}"
            )
            st.code(share_text, language="text")

    with st.expander("❓ 男性性の喜びと女性性の喜びの違いとは？"):
        st.write(
            "・**女性性の喜び（受容・感覚・愛される喜び）**:\n"
            "  人からの愛やサポートを「受け取る」、五感で美しさや心地よさを「味わう」、感情をのびやかに解放する喜びです。\n\n"
            "・**男性性の喜び（達成・行動・与える喜び）**:\n"
            "  目標に向かって「行動する」、課題を「達成する」、誰かに価値や優しさを「与える」という能動的なパワーの喜びです。\n\n"
            "・**統合エネルギー（自己統合・セルフパートナーシップ）**:\n"
            "  自らの意志で動き（自分彼氏）、そのプロセスや成果を心身全体で受け取る（自分彼女）という、内なる自分が相思相愛で巡っている最高の状態です。"
        )


if __name__ == "__main__":
    try:
        import streamlit as st
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            main_streamlit()
        else:
            cli_run()
    except Exception:
        cli_run()
