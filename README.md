# Horecast

- 競馬予想を見ることができるサイトです。
- AIによる競馬予想をみたり、予想の根拠となるデータを確認したり、他の人の予想を見ることができます。
- AIで使用している機械学習モデルはデータ収集からモデル構築まで一気通貫して自力で作成しました。

<img width="1680" alt="スクリーンショット 2021-11-01 11 29 16" src="https://user-images.githubusercontent.com/78991083/139613364-07883b87-765c-45fc-8f51-8e2f8d546ad5.png">

# 使用技術
(アプリ部分)
- HTML5
- CSS3
- Bootstrap5
- Javascript
- jQuery
- Python 3.8.8
- Django 3.2
- Dash 2.0.0
- PostgreSQL　12.4
![プロダクト構成図 001](https://user-images.githubusercontent.com/78991083/140001898-4c6687f6-8b6b-4784-a6e3-4f62a016678a.jpeg)

(モデル部分)
- Python 3.8.8
- Jupyter
- Beautiful Soup 4
- pandas 1.3.3
- Numpy 1.21.1
- seaborn 0.11.2
- matplotlib 3.4.3
- LightGBM
- OPTUNA
- scikit-learn 1.0

(その他)
- AWS Glue
- AWS S3

# 機能一覧

- AI予想表示機能
- 10分ごとに開催情報・レース結果・払戻金を受信して表示
- ダッシュボード（競馬場・コース距離ごとに枠順・騎手・調教師・種牡馬の勝率・連対率・複勝率を表示）
<img width="1680" alt="スクリーンショット 2021-11-03 11 26 04" src="https://user-images.githubusercontent.com/78991083/140002134-4f7af57c-45a6-4cb5-9409-ce18e661e5b2.png">

- 予想共有機能（予想を投稿・更新・確認・削除可能）
- 予想検索機能
<img width="1680" alt="スクリーンショット 2021-11-03 11 27 48" src="https://user-images.githubusercontent.com/78991083/140002210-bdfb1b31-9d8d-47b3-ae43-4336961bf1f7.png">

- ユーザ登録・ログイン機能
