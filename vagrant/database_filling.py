#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

engine = create_engine('sqlite:///beermenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Creating Beer categories and beer items
# Items for Ales
cat1 = Category(name="Ales")

session.add(cat1)
session.commit()

item1 = Item(name="Big Rig Gold", description="Our flagship beer is a refreshing golden brew that uses a blend of the finest Canadian and German malts giving it a smooth, mild body that balances the crisp, pleasant German hop finish.", category=cat1)

session.add(item1)
session.commit()

item2 = Item(name="Amsterdam Downtown Brown", description="British style brown ale. Blend of CDN, European & Chocolate malts from Belgium & 4 continental hops. Medium bodied dark beer gets some fine character from English ale yeast for a smooth traditional ale of chestnut brown colour with distinct drinkability", category=cat1)

session.add(item2)
session.commit()

item3 = Item(name="Belgian Moon", description="The award-winning US wheat beer comes to Canada. This delicious Belgian-Style witbier is brewed with malted barley, wheat and rolled oats. Coriander, along with Valencia and navel orange peels are added to create a smooth and refreshing, unfiltered wheat beer.", category=cat1)

session.add(item3)
session.commit()

# Items for Lagers
cat2 = Category(name="Lagers")

session.add(cat2)
session.commit()

item1 = Item(name="Amstel Light", description="Amstel Light is brewed in Amsterdam, part of brewing tradition that dates back to 1870. At just 95 calories per bottle. It's unique mixture of barley and hops delivers a full - never diluted - flavor that's just as tasty as regular beer.", category=cat2)

session.add(item1)
session.commit()

item2 = Item(name="Bavaria Extreme", description="Beer to the extreme, this rich, golden lager's taste is driven by huge malt notes.", category=cat2)

session.add(item2)
session.commit()

item3 = Item(name="Blue", description="Labatt Blue is a refreshing, pilsener-style lager brewed using John Labatt's founding philosophy that a quality beer should have a real, authentic taste. Blue is made with the finest hops and Canadian Barley malt.", category=cat2)

session.add(item3)
session.commit()

item4 = Item(name="Kozel", description="Kozel Premium Lager has a smooth, subtly bitter taste, a soft malt and hops scent and sparkles perfectly. This highly malted beer with an alcohol volume content of 5 Percent considered to be an excellent lager both at home and abroad.", category=cat2)

session.add(item4)
session.commit()

# Items for Malts
cat2 = Category(name="Malts")

session.add(cat2)
session.commit()

item1 = Item(name="Peach Mead", description="Peach Mead uses wild flower honey and peaches from Niagara to create this very refreshing Mead. The peach flavor is so fresh you can feel the peach fuzz against your teeth. Not overly sweet but delicate & floral, thanks to the pure Niagara honey.", category=cat2)

session.add(item1)
session.commit()

item2 = Item(name="Twisted Tea", description="Twisted Tea Brewing Company was founded on the twisted premise that a hard iced tea should taste like real iced tea. Imported from the U.S. Twisted Tea delivers an incredibly smooth and refreshing drinking experience in a 5 percent alc./vol. iced tea. Drinkers are amazed at how much it tastes like real iced tea.", category=cat2)

session.add(item2)
session.commit()

item3 = Item(name="Ginger Mead", description="Trafalgar Ginger Mead is a sparkling, spicy mead braggot that is unique in Ontario. We combine local honey, malt and hops with a prodigious amount of crushed ginger to produce this fascinating style.", category=cat2)

session.add(item3)
session.commit()

# Items for Stouts
cat2 = Category(name="Stouts")

session.add(cat2)
session.commit()

item1 = Item(name="Darkhorse Stout", description="Broadhead's Dark Horse Stout is a full-bodied, rich and creamy oatmeal stout that bristles with bold, unbridled taste. Blending roasted malt and oatmeal for a solid footing, this smooth, dark beer has shades of bitterness that gives Dark Horse the perfect edge.", category=cat2)

session.add(item1)
session.commit()

item2 = Item(name="Guinness Extra Stout", description="All the goodness of Guinness. A dark, full flavoured rich stout beer. Brewed under license from Guinness of Ireland.", category=cat2)

session.add(item2)
session.commit()


print("added beers and one user!")
