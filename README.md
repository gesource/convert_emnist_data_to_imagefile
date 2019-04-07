# convert_emnist_data_to_imagefile
emnistのデータをpng画像に変換して保存する

## Description

[emnist][1]のファイルを読み込んでpng画像に変換します。

[1]: https://www.westernsydney.edu.au/bens/home/reproducible_research/emnist "emnist"

emnistの画像の向きがおかしかったので、修正してから出力しています。

## Usage

引数に画像ファイル、ラベルファイル、作成した画像ファイルを保存するディレクトリを指定して、parse_mnist.pyを実行します。

python parse_emnist.py --image=emnist-mnist-train-images-idx3-ubyte --label=emnist-mnist-train-labels-idx1-ubyte --dir=images

引数dirで指定したディレクトリが作成され、その中にラベルごとのディレクトリが作成されます。 画像ファイルはラベルのディレクトリ内に作成されます。

## Requirement

Python 3.6.7で作成しました。
