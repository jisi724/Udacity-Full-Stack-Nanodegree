from models import db, User, Category, Item

# # init database
db.create_all()

# # fake some users
admin = User(
    username='admin',
    email='admin@category.com',
    avatar='https://www.w3schools.com/howto/img_avatar.png')
guest = User(
    username='guest',
    email='guest@category.com',
    avatar='''https://images.vexels.com/media/users/3/145908/preview2
    /52eabf633ca6414e60a7677b0b917d92-male-avatar-maker.jpg''')
db.session.add(admin)
db.session.add(guest)
db.session.commit()

# fake some categories
db.session.add_all([
    Category(title='Beauty'),
    Category(title='Books'),
    Category(title='Home & Garden'),
    Category(title='Major Appliances'),
    Category(title='Musical Instruments'),
    Category(title='Toys & Games'),
    Category(title='Video Games'),
    Category(title='Computers'),
    Category(title='Software'),
    Category(title='Fine Art'),
])
db.session.commit()

# fake some item
db.session.add_all([
    Item(
        title='MORPHE',
        desc='A setting mist to defend your makeup artistry. ',
        category_id=2,
        user_id=1),
    Item(
        title='Dear Zoo: A Lift-the-Flap Book',
        desc='''And with an updated look, this classic childrens
        storybook about a youngster loooking for a perfect pet is
        sure to delight a new generation of readers!''',
        category_id=3,
        user_id=1),
    Item(
        title='The Story of Spider-Man',
        desc='''The Story of the Amazing Spider-Man tells the tale of how Petet
         Parker came to have the powers and relative strength of a Spider!''',
        category_id=3,
        user_id=1),
    Item(
        title='Cocktail Table',
        desc='Ample surface space in a trendy natural reclaimed finish',
        category_id=4,
        user_id=1),
    Item(
        title='Glass Table',
        desc='Original and sturdy tempered glass base',
        category_id=4,
        user_id=2),
    Item(
        title='Mesh Chair',
        desc='Comfortable office chair with contoured mesh back for ability',
        category_id=4,
        user_id=1),
    Item(
        title='Pivot Vacuum',
        desc='Lithium Technology for strong suction and fade free power',
        category_id=5,
        user_id=1),
    Item(
        title='Pressure Cooker',
        desc='''All the features of the Instant Pot duo, the bestselling electric
        pressure cooker in North America now available in compact format.Power
        Supply Cord: 35 inches, detached, 3 prong plug''',
        category_id=5,
        user_id=2)
])
db.session.commit()
