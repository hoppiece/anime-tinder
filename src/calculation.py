from src.database import db
from src.models import User, LikeUnlike, AnimeData
from sqlalchemy import asc
import numpy as np
from typing import List


def user_anime_matrix():
    # user_idとanime_idを縦横にもち値がstatusの二次元配列を返す
    all_users = User.query.all()
    anime_num = len(AnimeData.query.all())
    user_id_list = [user.user_id for user in all_users]
    print("user_id_list:", user_id_list)
    res = []
    for user_id in user_id_list:
        # ユーザーひとりに対してアニメに対するlikeunlikeのstatusを取得, リストで保持する.
        lu_data = (
            db.session.query(LikeUnlike)
            .filter(LikeUnlike.user_id == user_id)
            .order_by(asc(LikeUnlike.anime_id))
            .all()
        )
        if lu_data is not None:
            # そのユーザーがlike_unlikeを一つでも設定しているなら
            user_status_list = []
            index = 1  # user_status_listの要素数は最終的にanime_numにならないといけないのでそのようにする
            for data in lu_data:
                data_anime_id = data.anime_id
                data_status = data.status
                # 前のループの次の場所からこのループのanime_idの場所まで0で埋める（デフォルト値）
                user_status_list.extend([0] * (data_anime_id - index))
                # このループのデータをいれる
                user_status_list.append(data_status)
                # インデックスを更新する
                index = data_anime_id + 1
            # 終わったら最後までを0で埋める.
            user_status_list.extend([0] * (anime_num + 1 - index))
        else:
            # 一つもlike_unlikeをしていないなら全て0で埋める
            user_status_list = [0] * anime_num
        res.append(user_status_list)
    # return jsonify(res) # 確認用
    # アニメID順にステータスが並んだリストがユーザーごとに並んでいる二次元リストを返す.
    return res


def anime_similarity():
    content_lu = np.array(user_anime_matrix()).T
    # anime_num, user_num = content_lu.shape[0], content_lu.shape[1]
    corr_mat = np.dot(content_lu, content_lu.T)
    anime_norm_vec = np.linalg.norm(content_lu, axis=1)
    anime_norm_mat = np.outer(anime_norm_vec, anime_norm_vec)
    anime_norm_mat = np.where(np.absolute(anime_norm_mat) < 0.001, anime_norm_mat, 1)
    cos_sim_mat = corr_mat / anime_norm_mat
    cos_sim_mat = cos_sim_mat - np.diag(cos_sim_mat, k=0)
    return cos_sim_mat


def collaborative_filtering(ith_anime: int, liked_anime_list: List[int]) -> int:
    # i 番目のアニメに対して、コサイン類似度ベースの協調フィルタリングでレコメンドされたアニメのid を返します。
    # 既にlike 済みのアニメは無視します
    cos_sim_mat = anime_similarity()
    recommend_vec = cos_sim_mat[ith_anime]
    recommend_vec[liked_anime_list] = 0
    recommend_id = np.argmax(recommend_vec)
    return recommend_id
