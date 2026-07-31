from werkzeug.security import generate_password_hash
from models import (db, User, Post, Movie, Game, Department, Course, AcademicNote,
                    PastQuestion, MCQ, DiscussionThread)

POSTER = {
    'interstellar': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTUy._V1_SX300.jpg',
    'inception': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
    'dune': 'https://m.media-amazon.com/images/M/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThhMGVjNzE2ZDE1XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_SX300.jpg',
    'parasite': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0YjYtZWE3MGZiM2NlN2E5XkEyXkFqcGdeQXVyNTc5OTMwOTQ@._V1_SX300.jpg',
    'godfather': 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SX300.jpg',
    'avatar': 'https://m.media-amazon.com/images/M/MV5BZDA0OGQxNTItMDZkMC00N1UyLWI0MjctNWM0NDVjNmE3ZDUyXkEyXkFqcGdeQXVyMTMxODk2OTUy._V1_SX300.jpg',
    'whiplash': 'https://m.media-amazon.com/images/M/MV5BOTA5NDZlZGUtMjAxOS00YTRkLTkwYmMtYWQ0NODZmMWU0NTk4XkEyXkFqcGdeQXVyNTA4NzY1MzY@._V1_SX300.jpg',
    'oppenheimer': 'https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2NzgtZDk2OWJkZWU0NTk5XkEyXkFqcGdeQXVyNTAyODQxNjk4._V1_SX300.jpg',
}

GAME_IMAGES = {
    'elden ring': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg',
    'baldur': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg',
    'god of war': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1593500/header.jpg',
    'cyberpunk': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg',
    'red dead': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1174180/header.jpg',
    'zelda': 'https://cdn.cloudflare.steamstatic.com/steam/apps/1284260/header.jpg',
    'hollow knight': 'https://cdn.cloudflare.steamstatic.com/steam/apps/367520/header.jpg',
    'stardew': 'https://cdn.cloudflare.steamstatic.com/steam/apps/413150/header.jpg',
}


def seed():
    if User.query.first():
        return

    alice = User(username='alice', password_hash=generate_password_hash('pass'), display_name='Alice Johnson', bio='Movie lover and CS student')
    bob = User(username='bob', password_hash=generate_password_hash('pass'), display_name='Bob Smith', bio='Gamer and football fan')
    carol = User(username='carol', password_hash=generate_password_hash('pass'), display_name='Carol Williams', bio='Future software engineer')
    db.session.add_all([alice, bob, carol])
    db.session.flush()

    posts = [
        Post(user_id=alice.id, content='Just watched Interstellar for the fifth time. That docking scene still gives me chills!'),
        Post(user_id=bob.id, content='Who wants to squad up on Elden Ring tonight? Need 2 more players.'),
        Post(user_id=carol.id, content='Final exams next week. The academic hub notes are saving my life right now!'),
        Post(user_id=alice.id, content='Dune Part 3 announcement? Best news this year!'),
        Post(user_id=bob.id, content='Just finished Baldur\'s Gate 3. 10/10 would romance a bear again.'),
    ]
    db.session.add_all(posts)

    movies = [
        Movie(title='Interstellar', release_year=2014, genre='Sci-Fi', rating=8.7, description='A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.', image_url=POSTER['interstellar']),
        Movie(title='Inception', release_year=2010, genre='Sci-Fi', rating=8.8, description='A thief who steals corporate secrets through dream-sharing technology.', image_url=POSTER['inception']),
        Movie(title='Dune: Part Two', release_year=2024, genre='Sci-Fi', rating=8.5, description='Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.', image_url=POSTER['dune']),
        Movie(title='Parasite', release_year=2019, genre='Thriller', rating=8.5, description='Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.', image_url=POSTER['parasite']),
        Movie(title='The Godfather', release_year=1972, genre='Crime', rating=9.2, description='The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.', image_url=POSTER['godfather']),
        Movie(title='Avatar', release_year=2009, genre='Sci-Fi', rating=7.9, description='A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.', image_url=POSTER['avatar']),
        Movie(title='Whiplash', release_year=2014, genre='Drama', rating=8.5, description='A promising young drummer enrolls at a cut-throat music conservatory.', image_url=POSTER['whiplash']),
        Movie(title='Oppenheimer', release_year=2023, genre='Drama', rating=8.4, description='The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.', image_url=POSTER['oppenheimer']),
    ]
    db.session.add_all(movies)
    db.session.flush()

    games = [
        Game(title='Elden Ring', genre='Action RPG', platform='PC, PS5, Xbox', rating=9.6, description='Rise, Tarnished, and be guided by grace to brandish the power of the Elden Ring and become an Elden Lord in the Lands Between.', image_url=GAME_IMAGES['elden ring']),
        Game(title="Baldur's Gate 3", genre='RPG', platform='PC, PS5', rating=9.7, description='Gather your party and return to the Forgotten Realms in a tale of fellowship and betrayal.', image_url=GAME_IMAGES['baldur']),
        Game(title='God of War Ragnarok', genre='Action', platform='PS5, PC', rating=9.4, description='Kratos and Atreus must journey to each of the Nine Realms in search of answers.', image_url=GAME_IMAGES['god of war']),
        Game(title='Cyberpunk 2077', genre='Open World RPG', platform='PC, PS5, Xbox', rating=9.1, description='V is a mercenary out for one last score — the ultimate implant that gives the key to immortality.', image_url=GAME_IMAGES['cyberpunk']),
        Game(title='Red Dead Redemption 2', genre='Open World', platform='PC, PS4, Xbox', rating=9.7, description='America, 1899. Arthur Morgan and the Van der Linde gang are outlaws on the run.', image_url=GAME_IMAGES['red dead']),
        Game(title='The Legend of Zelda: Tears of the Kingdom', genre='Adventure', platform='Switch', rating=9.6, description='An epic adventure across the land and skies of Hyrule.', image_url=GAME_IMAGES['zelda']),
        Game(title='Hollow Knight', genre='Metroidvania', platform='PC, Switch', rating=9.0, description='Forge your own path in a beautiful, devastated world held together by insect gods.', image_url=GAME_IMAGES['hollow knight']),
        Game(title='Stardew Valley', genre='Farming Sim', platform='PC, Switch, Mobile', rating=9.2, description='You\'ve inherited your grandfather\'s old farm plot in Stardew Valley.', image_url=GAME_IMAGES['stardew']),
    ]
    db.session.add_all(games)

    depts = [
        ('Computer Science', 'CS', 'Study of computation, algorithms, and software systems.'),
        ('Mathematics', 'MATH', 'The abstract science of number, quantity, and space.'),
        ('Physics', 'PHYS', 'The natural science that studies matter and energy.'),
        ('Engineering', 'ENG', 'Applied science, technology, and problem solving.'),
        ('Business Administration', 'BUS', 'Management, finance, and organizational studies.'),
        ('Biology', 'BIO', 'The study of living organisms and life processes.'),
        ('Economics', 'ECON', 'The study of production, distribution, and consumption.'),
        ('Law', 'LAW', 'The study of legal systems and justice.'),
        ('Medicine', 'MED', 'The science and practice of diagnosing and treating disease.'),
        ('Literature', 'LIT', 'The study of written works and creative expression.'),
        ('Chemistry', 'CHEM', 'The study of substances and their properties.'),
        ('Psychology', 'PSY', 'The scientific study of the mind and behavior.'),
    ]
    departments = [Department(name=n, code=c, description=d) for n, c, d in depts]
    db.session.add_all(departments)
    db.session.flush()

    cs = departments[0]
    courses = [
        Course(department_id=cs.id, code='CS101', title='Introduction to Programming', description='Fundamentals of programming using Python.', semester='Sem 1'),
        Course(department_id=cs.id, code='CS201', title='Data Structures & Algorithms', description='Arrays, linked lists, trees, graphs, and algorithm analysis.', semester='Sem 3'),
        Course(department_id=cs.id, code='CS301', title='Database Systems', description='Relational databases, SQL, and database design.', semester='Sem 4'),
    ]
    db.session.add_all(courses)
    db.session.flush()

    notes = [
        AcademicNote(course_id=courses[0].id, title='Variables and Data Types', content='Python has int, float, str, bool, list, tuple, dict, set. Use type() to check a variable\'s type.'),
        AcademicNote(course_id=courses[0].id, title='Functions in Python', content='def function_name(params): ... return value. Default arguments and *args/**kwargs.'),
        AcademicNote(course_id=courses[1].id, title='Big O Notation', content='O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n), O(n^2) quadratic.'),
        AcademicNote(course_id=courses[2].id, title='SQL Joins', content='INNER JOIN returns matching rows, LEFT JOIN returns all from left table, RIGHT JOIN all from right.'),
    ]
    db.session.add_all(notes)

    past_questions = [
        PastQuestion(course_id=courses[0].id, title='Midterm 2024', content='1. Write a program to reverse a string.\n2. Explain mutable vs immutable types.', exam_year=2024),
        PastQuestion(course_id=courses[1].id, title='Final 2023', content='1. Implement quicksort.\n2. Explain the time complexity of BFS.', exam_year=2023),
    ]
    db.session.add_all(past_questions)

    mcqs = [
        MCQ(course_id=courses[0].id, question='Which data type is immutable in Python?', option_a='list', option_b='tuple', option_c='dict', option_d='set', correct_answer='B'),
        MCQ(course_id=courses[1].id, question='What is the time complexity of binary search?', option_a='O(n)', option_b='O(log n)', option_c='O(n log n)', option_d='O(1)', correct_answer='B'),
        MCQ(course_id=courses[2].id, question='Which SQL keyword joins tables?', option_a='MERGE', option_b='JOIN', option_c='LINK', option_d='COMBINE', correct_answer='B'),
    ]
    db.session.add_all(mcqs)

    thread = DiscussionThread(course_id=courses[0].id, title='Best way to learn Python?', content='I\'m new to programming. Should I start with loops or functions first?', author_id=carol.id)
    db.session.add(thread)

    db.session.commit()
