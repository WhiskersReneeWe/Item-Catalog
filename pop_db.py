
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_setup import Base, Category, Item, User



engine = engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(username='Renee Liu', email = 'reneesyliu@gmail.com')
session.add(user1)
session.commit()

user_genesis = session.query(User).filter_by(email='reneesyliu@gmail.com').one()

cate1 = Category(name='Soccer', user_id = user_genesis.id)
session.add(cate1)
session.commit()


item1 = Item(name = "FIFA shirt women", description = "FIFA marks on the back and a big pink ball on the front",\
             user_id = user_genesis.id, category = cate1)
session.add(item1)
session.commit()

item2 = Item(name = "FIFA shirt men", description = "FIFA marks on the back and a big black heart on the front", \
             user_id = user_genesis.id, category = cate1)
session.add(item2)
session.commit()

cate2 = Category(name='Basketball', user_id = user_genesis.id)
session.add(cate2)
session.commit()


item1 = Item(name = "Nike Leather Basketballs", description = "Made out of fake leather", \
             user_id = user_genesis.id, category = cate2)
session.add(item1)
session.commit()

item2 = Item(name = "Oversized Basketball vests", description = "rainball colors with different sizes", \
             user_id = user_genesis.id, category = cate2)
session.add(item2)
session.commit()

cate3 = Category(name='Baseball', user_id = user_genesis.id)
session.add(cate3)
session.commit()


item1 = Item(name = "Yankee hats", description = "all hats are designer hats and the materials are extremely recyclable", \
             user_id = user_genesis.id, category = cate3)
session.add(item1)
session.commit()

item2 = Item(name = "baseballs bats", description = "Different colors are available. You can also pre-order with your chosen color",\
             user_id = user_genesis.id, category = cate3)
session.add(item2)
session.commit()

cate4 = Category(name='Snowboarding', user_id = user_genesis.id)
session.add(cate4)
session.commit()


item1 = Item(name = "Goggles", description = "Goggles are made out of lime stones, and they all are imported from Netherland", \
             user_id = user_genesis.id, category = cate4)
session.add(item1)
session.commit()

item2 = Item(name = "Snowboards", description = "Different Length and different designs are available for all professional levels", \
             user_id = user_genesis.id, category = cate4)
session.add(item2)
session.commit()

cate5 = Category(name='Swimming', user_id = user_genesis.id)
session.add(cate5)
session.commit()


item1 = Item(name = "Swimming suits", description = "Roxy brands and alike are available. \
                       They are made out of materials that are environmentally friendly", \
             user_id = user_genesis.id, category = cate5)
session.add(item1)
session.commit()

item2 = Item(name = "Swimming Goggles", description = "They are all on sale. Different colors are available", 
             user_id = user_genesis.id, category = cate5)
session.add(item2)
session.commit()

cate6 = Category(name='Hockey', user_id = user_genesis.id)
session.add(cate6)
session.commit()

cate7 = Category(name='Skating', user_id = user_genesis.id)
session.add(cate7)
session.commit()

cate8 = Category(name='Football', user_id = user_genesis.id)
session.add(cate8)
session.commit()

cate9 = Category(name='Rock Climbing', user_id = user_genesis.id)
session.add(cate9)
session.commit()


# Check initial database setup is successful
print("ItemCatalog Database populated!")
print("Checking Catagories ...")
cates = session.query(Category).all()
for cate in cates:
    print('{} has the following items'.format(cate.name))
    items = session.query(Item).filter_by(category = cate).all()
    for item in items:
        print(item.name)
