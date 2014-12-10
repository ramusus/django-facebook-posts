--facebook_posts_post_likes_users

CREATE UNIQUE INDEX facebook_posts_post_likes_users_time_from_3col_uniq
ON facebook_posts_post_likes_users (post_id, user_id, time_from)
WHERE time_from IS NOT NULL;

CREATE UNIQUE INDEX facebook_posts_post_likes_users_time_from_2col_uniq
ON facebook_posts_post_likes_users (post_id, user_id)
WHERE time_from IS NULL;

CREATE UNIQUE INDEX facebook_posts_post_likes_users_time_to_3col_uniq
ON facebook_posts_post_likes_users (post_id, user_id, time_to)
WHERE time_to IS NOT NULL;

CREATE UNIQUE INDEX facebook_posts_post_likes_users_time_to_2col_uniq
ON facebook_posts_post_likes_users (post_id, user_id)
WHERE time_to IS NULL;

--facebook_posts_post_shares_users

CREATE UNIQUE INDEX facebook_posts_post_shares_users_time_from_3col_uniq
ON facebook_posts_post_shares_users (post_id, user_id, time_from)
WHERE time_from IS NOT NULL;

CREATE UNIQUE INDEX facebook_posts_post_shares_users_time_from_2col_uniq
ON facebook_posts_post_shares_users (post_id, user_id)
WHERE time_from IS NULL;

CREATE UNIQUE INDEX facebook_posts_post_shares_users_time_to_3col_uniq
ON facebook_posts_post_shares_users (post_id, user_id, time_to)
WHERE time_to IS NOT NULL;

CREATE UNIQUE INDEX facebook_posts_post_shares_users_time_to_2col_uniq
ON facebook_posts_post_shares_users (post_id, user_id)
WHERE time_to IS NULL;
