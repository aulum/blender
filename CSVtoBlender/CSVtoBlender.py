import bpy  # blenderのpythonをインストール
import csv
import math


"""
※注意※

このスクリプトはネクストシステム様のミチコンPlusから出力したCSVデータをblenderのモデルに読み込ませるためのものです。
69行目のcsvのパスを書き換えて使用してください。
また、以下の4点に注意して使用してください。

①骨の名前はCSVの一行目と同じ名前にしてください。ボーンが存在しなければ無視します。
例：Hips,Spine,Chest　など

②CSVを焼き付けたいボーンを選択してからスクリプトを使用してください。

③CSVはblenderを保存しているドライブ内にしてください。
→別のドライブにしてると失敗します。なぜなのかわかってないので調べます…。

④現在のフレームからベイクが開始します。

"""

# カレントフレームをシーンの開始フレームに設定
frame_cur = (bpy.context.scene.frame_start)
bpy.context.scene.frame_set(frame_cur)
# 選択したオブジェクトに名前をつける
arm = bpy.context.active_object
# 選択したオブジェクトの骨を選ぶ
boneNames = list(map(lambda bone: bone.name, arm.data.bones))
psbone = arm.pose.bones

# ポーズモードにする
bpy.ops.object.mode_set(mode='POSE')
# 下準備ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー


def rotateBone(time, boneName, z, x, y):
    # 骨がなかったら終了
    if boneName not in boneNames:
        print(boneName)
        return
    # 骨を選択
    arm.data.bones[boneName].select = True
    # クオータニオンからYXZに変換する
    psbone[boneName].rotation_mode = 'ZXY'
    # 回転させる
    psbone[boneName].rotation_euler = (
        math.radians(z), math.radians(x)*-1, math.radians(y))
    # 新しいフレームにセット
    psbone[boneName].keyframe_insert(frame=time, data_path='rotation_euler')
    print(str(time)+" "+boneName+" done")


def moveBone(time, boneName, z, x, y):
    # 骨がなかったら終了
    if boneName not in boneNames:
        print(boneName)
        return
    # 移動させる
    psbone[boneName].location = (z*100, x, y*100)
    # 新しいフレームにセット
    psbone[boneName].keyframe_insert(frame=time, data_path='location')
    print(str(time)+" "+boneName+" done")


# CSVを開いて行と列にデータをそれぞれおさめる
with open("C:\sample.csv") as f:
    # タイトルのヘッダーは飛ばす
    boneList = next(csv.reader(f))
    reader = csv.reader(f)
    # csvの各行ごとにloop
    for row in reader:
        # 時間を取得
        time = float(row[0])
        # Hipsの処理
        hipsZ, hipsX, hipsY = [float(value) for value in row[1].split(' ')]
        moveBone(time*10, boneList[1], hipsZ, hipsX, hipsY)
        for columnIndex, zxy in enumerate(row[2:], 2):
            # zxy = “0.1 0.2 0.3”
            # zxy.split(‘ ‘) = [“0.1”, ”0.2”, “0.3”]
            # [float(value) for value in zxy.split(‘ ‘)] = [0.1,0.2,0.3]
            # z, x, y = [0.1, 0.2, 0.3]   (多重代入)
            # cellの値をparse
            z, x, y = [float(value) for value in zxy.split(' ')]
            # 骨を動かす
            # boneList[columnIndex] = 骨の名前
            rotateBone(time*10, boneList[columnIndex], z, x, y)
