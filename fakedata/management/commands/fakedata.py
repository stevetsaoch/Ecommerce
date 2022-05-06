from decimal import *
import random
import uuid
import shortuuid
from django.core.management.base import BaseCommand
from account.models import UserBase, Address
from orders.models import Order, OrderItem
from checkout.models import DeliveryOptions, PaymentSelections
from store.models import Product
from review.models import Review
from django_countries import countries
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    def __init__(self):
        self.first_name = [
            "Peter",
            "Bruce",
            "Steve",
            "Roy",
            "Carol",
            "James",
            "Benkamin",
            "Robert",
            "Mark",
            "Anna",
            "Allen",
        ]
        self.last_name = [
            "Parker",
            "Banner",
            "Rogers",
            "Thomas",
            "Danvers",
            "Logan",
            "Grimm",
            "Reynodls",
            "Spector",
            "Delvey",
            "Chlumsky",
        ]

        self.countries_code = list(dict(countries).keys())

        self.city = [
            "Gotham City",
            "Taipei",
            "New York City",
            "Lodon",
            "New Mexico State",
            "Sydney",
            "Queensland",
            "Los Angeles",
            "Chicago",
            "Taichung",
        ]

        self.address_line = [
            "Lang Avenue",
            "Straford Park",
            "Seneca Drive",
            "Linden Avenue",
            "Stiles Street",
            "Prospect Street",
            "Charack Road",
            "Walkers Ridge Way",
        ]

        self.address_line2 = [
            "531E 31st Alley",
            "12B 3rd Lane",
            "51A 1st Alley",
            "53C 22nd Lane",
            "42E 11th Sub-Alley",
            "23F 68th Alley",
            "86G 83rd Sub-Alley",
        ]

        self.review = {
            "1": {
                "line1": [
                    [
                        "This book read like a compilation of infographics. It helped introduce a number of concepts but very lightly touched on these basics. "
                    ],
                    [
                        "I agree with other reviewers that while yes this is an amazing book and one that I would recommend - the binding is awful. Within a week my book cover curled and has never uncurled. The paperback book falls apart despite the most careful breaking in of the book- I used to work as a librarian so I know how to treat my books."
                    ],
                    [
                        "The glossy paper makes it impossible to read in anything but daylight, there is white print on black pages, black print on blue pages, light blue print on glossy white pages - it looks like a mishmash of graphic design exercises."
                    ],
                ],
                "line2": [
                    [
                        " SOME information about ",
                        ' shared, NO exercises or actual "web design or building", and feeling like you have hardly learned anything. Pass on this one.',
                    ],
                    [
                        " Last, as to content, it was so difficult to read I just skimmed it. But I'm already more up to date than this weak technical book. There are many competitive choices out there for superior content. I'm sending it right back."
                    ],
                    [
                        "Maybe it is just cruising on momentum of good reviews from years gone by. Anyway, I would recommend another book instead."
                    ],
                ],
            },
            "2": {
                "line1": [
                    [
                        "Interesting book, but lacks a lot of explanation. Ultimately just another glorified ",
                        " book, some of which are helpful. Lack of clarity lets it down unfortunately.",
                    ],
                    [
                        "The pictures of text that we are told to write down towards the beginning are so small it ridiculous. For the rest of the book, the font is too thin and too small for me to comfortably read."
                    ],
                    [
                        "I agree with the majority of the comments about the layout and information presented in this book. The problem is that much of the information is outdated."
                    ],
                    [
                        "I bought this based on the other reviews that it was aimed at teaching the general features of ",
                        ", so that I could improve my skills with these languages. What I got was a VERY HEAVY, HARD TO READ BOOK with a lot of unnecessary pictures and white space, hard to read instructions because of font colors and size, and some information that was hard to transfer to other applications.",
                    ],
                ],
                "line2": [
                    [
                        " To sum up, if you want a graphic coffee table book about html to impress your friends with how pretty it is and how smart you are, get this book. If you actually want to learn the subject matter, look elsewhere."
                    ],
                    [
                        " Finally, if you have ever written any of the most basic ",
                        " then you already know more than this book will teach you.",
                    ],
                    [
                        " One other negative. Even after only glancing through the book to see what it was like, the front cover deformed significantly so that the book looked well used. Not very good for a trade in, which I am going to do."
                    ],
                    [
                        " Last, unfortunately at the time this book was written ",
                        " had not been implemented and responsive design which is so critical now is barely mentioned.",
                    ],
                ],
            },
            "3": {
                "line1": [
                    [
                        "Book I received didn't look and feel like an illegal physical copy or a rather poor quality physical product, 3 stars here is for the crappy production quality and not for the content."
                    ],
                    [
                        "I loved about 60% of this book. The author is direct, straight to the point... Quite opinionated too. He's quite clear about what is good ",
                        " and what is bad. I learned a lot. He lost me towards the last third of the book where he starts repeating himself. The appendices are again a repeat of the first chapters.",
                    ],
                    [
                        "There is no explanation of concepts, this is merely a treatise on what the book's title states: The Good Parts of ",
                        ". The reader should be aware that this will only be what is discussed and nothing more.",
                    ],
                    [
                        "Among all the books on ",
                        " this one is definitely not the best. Even though second part goes much deeper than any other textbook I could find.",
                    ],
                    [
                        "I am new to ",
                        " but it’s a lot less concept heavier than I expected. It assumes you know most of the concept to begin with.",
                    ],
                ],
                "line2": [
                    [
                        " Also, The author's statement strongly discourages anyone who wants to contribute to ",
                        " or needs some insights or explanation of these model behavior and outcome. No wonder why there are so many code monkeys out there in the industry.",
                    ],
                    [" To sum it up, there were things I didn't like but I still recommend reading it."],
                    [
                        " However, if you're an intermediate ",
                        " programmer, or an expert in another language, you'll get a lot out of this. If you're neither, you'll get nothing out of it.",
                    ],
                    [
                        " Overall, if you have the money to buy other books to learn ",
                        ", avoid this one. It is like having a bunch of sticky notes for stuff you already should know if you are a programmer. If you are looking to seriously learn ",
                        ", there are many better options that will tech you a lot more and be just as good of references.",
                    ],
                    [
                        " Plus, many important details are either missing or just glossed over. The code samples are riddled with mistakes and typos."
                    ],
                ],
            },
            "4": {
                "line1": [
                    [
                        "Very wordy but probably covers all there is to know. Better as a reference tome than a tutorial."
                    ],
                    [
                        "Wanted an overall intro to ",
                        " beyond either the childishly simple or something directed at the professional developer.",
                    ],
                    [
                        'I did expect different things from this book to be honest - I thought I\'d get a reference book. Someone called this a "collection of stories" which is pretty accurate - you will learn in depth ',
                        " but not very well organised.",
                    ],
                    [
                        " It is a help in understanding but it is also confusing at times because the topics are not always clear in what or how to work with a certain element or action."
                    ],
                    [
                        "The book serves as very good soft introduction to ",
                        ". It focuses on intuition over mathematics and example over theory. The example over theory philosophy goes perhaps too far in my opinion, as I feel the book leaves the reader with a very limited understanding of how things *actually work*.",
                    ],
                ],
                "line2": [
                    [
                        ' Although, I am still learning I find this book to be simple and easy to follow with explanations that aren’t too "techy". I appreciate the suggestions and options offered as well as links to see things "in action"'
                    ],
                    [
                        " In addition, 20 pages in the middle of my book were faint and very hard to read - an obvious printing error. My copy is the first printing!"
                    ],
                    [
                        " Besides, here is some weirdness with the layout; many words are hyphenated when they don't need to be, such as in the middle of a sentence. Minor nit that they will hopefully fix in the next printing."
                    ],
                    [
                        " As a whole, there is a lot in this book that will keep any ",
                        " student or practitioner busy. The sample code and detailed explanations are perfect reference material for current and future projects.",
                    ],
                    [
                        ' So, why the four stars? Because the book is rather "paint by the numbers". The presentation is filled with "Now you\'ll do this.." followed by working blocks of code for the student to enter and run. But there are no exercises.'
                    ],
                ],
            },
            "5": {
                "line1": [
                    [
                        "If you can only buy one book on ",
                        ",this should be the one you buy. No single book will cover everything, but this one has done the best job of covering the basics of everything(and much more).",
                    ],
                    [
                        "Many features of ",
                        " are explored here, and doing it by example makes the book much more interesting.",
                    ],
                    ["As a mid-career software professional trying to get into ", ", this book is pure Gold."],
                    [
                        "In all honesty, I love this book so much. Currently studying for ",
                        " and it comes in really handy, of course there are many concepts I'm entirely new to in the textbook but I believe with time, I'll be comfortable with it.",
                    ],
                    [
                        "This book is a complete reference on state-of-art ",
                        " unlike some reviewers indicated otherwise. Most of subjects in the area were covered and explained well. I don't know if any other expert could describe all these material better.",
                    ],
                    [
                        "It was a great walkthrough to learn ",
                        ", and how to start in a scenario and consider many different approaches improving step by step, evolving from simple things to a complete solution.",
                    ],
                ],
                "line2": [
                    [
                        " Overall this is the best book I've read on",
                        " .Most books leave out specifics in their projects. This book instead forgoes explaining css/bootstrap and focuses on explaining how the ",
                        "works while building multiple projects from start to finish.",
                    ],
                    [
                        " Lastly, This edition is spot on, and I haven't found an error yet after finishing the first 3 projects. It's a big time investment to actually go through and follow all the steps in creating the projects, but it's well worth it."
                    ],
                    [
                        " Overall, The presentation style is very didactic suitable for students, allowing to go different ways from a scenario and value the different results on their own."
                    ],
                    [
                        " In conclusion, finding a great resource like this one will save you many headaches and hours of research. Do yourself a favor and buy this book. It's worth every penny I paid!"
                    ],
                    [
                        " Plus, it doesn`t waste time teaching you things that you don`t need to know, it is a common mistake when authors, for the sake of filling out pages, overwhelm the reader with unnecessary info."
                    ],
                ],
            },
        }

    def random_phone_number(self):
        phone_number = "+886"

        for i in range(1, 10):
            phone_number += str(random.randint(0, 9))

        return phone_number

    def random_postcode(self):
        postcode = ""

        for i in range(1, 6):
            postcode += str(random.randint(0, 9))

        return postcode

    def random_item(self, num) -> dict:
        products = Product.objects.all()
        random_products = random.sample(list(products), k=num)
        total_paid = Decimal(0.00)
        for product in random_products:
            total_paid += product.price

        return {"products": random_products, "total_paid": total_paid}

    def random_review(self, rating, product_category: str) -> str:
        review = self.review[str(rating)]
        line1 = random.choice(review["line1"])
        line2 = random.choice(review["line2"])
        if line1.__len__() > 1:
            line1 = product_category.join(line1)
        else:
            line1 = line1[0]

        if line2.__len__() > 1:
            line2 = product_category.join(line2)
        else:
            line2 = line2[0]

        final_line = line1 + "\n" + line2
        return final_line

    def add_arguments(self, parser):
        parser.add_argument("--createFakeUsers", action="store_true", help="create fake users")
        parser.add_argument("--userNumber", type=int, default=0, help="number of user to create")
        parser.add_argument("--createFakeOrders", action="store_true", help="create fake orders")
        parser.add_argument("--orderNumber", type=int, default=0, help="number of order to create")
        parser.add_argument("--createFakeReviews", action="store_true", help="create fake users")
        parser.add_argument("--reviewNumber", type=int, default=0, help="number of review to create")

    def handle(self, *args, **options):
        if options["createFakeUsers"]:
            number = options["userNumber"]
            i = 1
            while i < number:
                ids = UserBase.objects.all().values_list("id", flat=True)

                # create fake user
                max_user_id = max(ids)
                first_name = random.choice(self.first_name)
                last_name = random.choice(self.last_name)
                userinfo = {
                    "id": max_user_id + 1,
                    "email": first_name + last_name + "@a.com",
                    "user_name": first_name + last_name,
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": 1,
                    "profile_img": "images/fakedata/profile" + str(random.randint(0, 9)) + ".png",
                }
                user = UserBase(**userinfo)
                user.set_password("qazxcv123")
                user.save()

                # create fake user address
                addressinfo = {
                    "id": uuid.uuid4(),
                    "customer": user,
                    "full_name": userinfo["first_name"] + " " + userinfo["last_name"],
                    "country": random.choice(self.countries_code),
                    "phone": self.random_phone_number(),
                    "town_city": random.choice(self.city),
                    "postcode": self.random_postcode(),
                    "address_line": random.choice(self.address_line),
                    "address_line2": random.choice(self.address_line2),
                }

                address = Address(**addressinfo)
                address.save()
                i += 1

        if options["createFakeOrders"]:
            number = options["orderNumber"]
            i = 1
            while i < number:
                # Pick up a user randomly
                users = UserBase.objects.all()
                user_instance = random.choice(users)

                # get address of user
                address_instance = Address.objects.get(customer_id=user_instance.id)

                # get delivery method
                deliveryoptions_instance = DeliveryOptions.objects.all()
                deliveryoptions_instance = random.choice(deliveryoptions_instance)

                # get payment method
                payment_instance = PaymentSelections.objects.all()

                # get items
                products = self.random_item(random.choice(list(range(1, 6))))

                order = {
                    "id": max(Order.objects.all().values_list("id", flat=True)) + 1,
                    "user": user_instance,
                    "address": address_instance,
                    "delivery_option": deliveryoptions_instance,
                    "payment_option": random.choice(payment_instance),
                    "email": user_instance.email,
                    "total_paid": products["total_paid"] + deliveryoptions_instance.delivery_price,
                    "order_key": shortuuid.uuid(),
                    "billing_status": True,
                }

                order_new = Order(**order)
                order_new.save()

                for product in products["products"]:
                    OrderItem.objects.create(order=order_new, product=product, quantity=1)

                i += 1

        if options["createFakeReviews"]:
            number = options["reviewNumber"]
            i = 1
            while i < number:
                # define a user from order item model
                order_id = random.choice(OrderItem.objects.all().values_list("order_id", flat=True))
                user_id = Order.objects.get(id=order_id).user_id
                user_instance = UserBase.objects.get(id=user_id)

                # products
                product_ids = OrderItem.objects.filter(order_id=order_id).values_list("product_id", flat=True)
                if product_ids.__len__() > 1:
                    product_id = random.choice(product_ids)
                else:
                    product_id = product_ids[0]
                
                # product instance
                product_instance = Product.objects.get(id=product_id)
                try:
                    review = Review.objects.filter(product_id=product_id).get(reviewer_id=user_id)

                except ObjectDoesNotExist:
                    # rating
                    rating = random.choice([1, 2, 3, 4, 5])

                    review = self.random_review(rating, product_instance.category.name)
                    review_info = {
                        "reviewer": user_instance,
                        "product": product_instance,
                        "review_text": review,
                        "rating": rating,
                    }
                    review = Review(**review_info)
                    review.save()
                    i += 1
                else:
                    print("review exist")

