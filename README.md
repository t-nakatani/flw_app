# flwapp(花画像から花弁の配置を推定するwebアプリケーション)


#### 学習済み weight を配置
git cloneした後に，infer/yolov5の直下に[exp21_best.pt](https://drive.google.com/file/d/1nvThW-V4XxmE8podHrJugb6a4zZN2FTL/view?usp=sharing)を配置

#### docker image の作成
`docker build -t flw_app:latest .`
#### docker container の作成
`docker run -it -v $(pwd):/work -p 8000:8000 flw_app:latest /bin/bash`

#### flw_app の起動
flwappの直下で

`python manage.py migrate`

`python manage.py runserver 0.0.0.0:8000`

http://localhost:8000/home/ にアクセス

This repository inherited https://github.com/t-nakatani/flwapp_nakatani_old
