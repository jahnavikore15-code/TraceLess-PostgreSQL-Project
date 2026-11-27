CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS platforms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    category VARCHAR(60) NOT NULL DEFAULT 'Other'
);

CREATE TABLE IF NOT EXISTS user_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform_id INTEGER NOT NULL REFERENCES platforms(id),
    username VARCHAR(150) NOT NULL,
    last_used DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    account_id INTEGER REFERENCES user_accounts(id) ON DELETE SET NULL,
    activity_type VARCHAR(100) NOT NULL,
    activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS privacy_checks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    is_done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO privacy_checks(user_id, title)
SELECT u.id, seed.title
FROM users u
CROSS JOIN (VALUES
 ('I use unique passwords for important accounts'),
 ('Two-factor authentication is enabled where available'),
 ('I reviewed app permissions recently'),
 ('I removed accounts I no longer use')
) AS seed(title)
WHERE NOT EXISTS (SELECT 1 FROM privacy_checks pc WHERE pc.user_id=u.id);
