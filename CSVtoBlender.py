import bpy  # blenderのpythonをインストール
import csv
import math


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
