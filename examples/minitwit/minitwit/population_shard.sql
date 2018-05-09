INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('839b83a4-abce-44e2-b506-7d40c0d937c1'),'swati', 'swati@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('ad98530c-b419-43f2-be2a-e4c1150da80c'),'sachin', 'sachin@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('ca5ef9e1-41e9-49c6-900c-34aea6edaa12'),'satish', 'satish@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('12638541-fc9e-4267-921c-2ef99bdab6f0'),'saket', 'saket@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('d909ba1b-9199-440d-9bfa-3c3c2a8e0826'),'disu', 'disu@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO user (user_id,username, email, pw_hash)
VALUES (UUID('c29001eb-7f30-479e-afab-3e62e59f1e4f'),'nani', 'nani@gmail.com', 'pbkdf2:sha256:50000$K44zojNm$aad044ee1a5c1be1eb3bfdf4af2f370717519669c5cb8e5e48e7131229553c2b');

INSERT INTO follower
VALUES (UUID('839b83a4-abce-44e2-b506-7d40c0d937c1'), UUID('ad98530c-b419-43f2-be2a-e4c1150da80c'));

INSERT INTO follower
VALUES (UUID('839b83a4-abce-44e2-b506-7d40c0d937c1'), UUID('ca5ef9e1-41e9-49c6-900c-34aea6edaa12'));

INSERT INTO follower
VALUES (UUID('ad98530c-b419-43f2-be2a-e4c1150da80c'), UUID('ca5ef9e1-41e9-49c6-900c-34aea6edaa12'));

INSERT INTO follower
VALUES (UUID('12638541-fc9e-4267-921c-2ef99bdab6f0'), UUID('ca5ef9e1-41e9-49c6-900c-34aea6edaa12'));

INSERT INTO follower
VALUES (UUID('d909ba1b-9199-440d-9bfa-3c3c2a8e0826'), UUID('839b83a4-abce-44e2-b506-7d40c0d937c1'));

INSERT INTO follower
VALUES (UUID('ca5ef9e1-41e9-49c6-900c-34aea6edaa12'), UUID('ad98530c-b419-43f2-be2a-e4c1150da80c'));

INSERT INTO message (author_id, text, pub_date)
VALUES (UUID('839b83a4-abce-44e2-b506-7d40c0d937c1'), 'Hey everyone!', 100); 

INSERT INTO message (author_id, text, pub_date)
VALUES (UUID('ad98530c-b419-43f2-be2a-e4c1150da80c'), 'Hey! Goodmorning!', 100);

INSERT INTO message (author_id, text, pub_date)
VALUES (UUID('d909ba1b-9199-440d-9bfa-3c3c2a8e0826'), 'Have a great day guys!', 100); 

