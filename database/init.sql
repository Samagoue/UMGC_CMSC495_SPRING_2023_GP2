-- Insert some users
-- password1 = 0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e
-- password2 = 6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4
-- password3 = 5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764
INSERT OR IGNORE INTO users (first_name, last_name, username, email, password, dob, is_admin) VALUES
    ('Alice', 'Anderson', 'aanderson', 'alice@example.com', '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', '1990-01-01', 0),
    ('Bob', 'Brown', 'bbrown', 'bob@example.com', '6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', '1991-02-02', 0),
    ('Charlie', 'Chaplin', 'cchaplin', 'charlie@example.com', '5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764', '1992-03-03', 1);

-- Insert some events
INSERT INTO events (name, date, type) VALUES
    ('Birthday Party', '2023-06-01', 'Party'),
    ('Graduation Ceremony', '2023-07-01', 'Academic'),
    ('Company Picnic', '2023-08-01', 'Corporate');

-- Insert some wishlists
INSERT INTO wishlist (user_id, event_id, wish) VALUES
    (1, 1, 'A new bike'),
    (1, 2, 'A trip to Europe'),
    (2, 1, 'A new laptop'),
    (2, 2, 'A new camera');

-- Insert some groups
INSERT INTO groups (group_name, min_dollar_amount) VALUES
    ('Family', 50),
    ('Friends', 20),
    ('Colleagues', 10);

-- Insert some pairs
INSERT INTO pairs (giver_id, receiver_id, event_id, group_id) VALUES
    (1, 2, 1, 1),
    (2, 1, 1, 1),
    (3, 1, 3, 3),
    (1, 3, 1, 2);

-- Insert some user-group relationships
INSERT INTO user_groups (user_id, group_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (3, 3);

-- Insert some user-event relationships
INSERT INTO user_events (user_id, event_id) VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (3, 3);
