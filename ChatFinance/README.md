<<<<<<< HEAD
> > 1.  setup conda virtual env, develop within conda env

> > 2.  environment setup

    # install dependencies listed in requirements.txt

    pip install -r requirements.txt
    pip install openai
    export OPENAI_API_KEY="your_openai_api_key"

    # setup MongoDB, (need install mongosh if using mongosh for interacting with MongoDB)

    #use dockerized MongoDB
    . install Docker first
    . setup Dockerized MongoDB :
    docker pull mongo
    docker run -d --name mongodb -p 27017:27017 mongo # container name: mongodb, mongodb default port 27017

> > 3.  connect to the mongoDB container using mongosh (another option: connect to mongodb by Using Python with PyMongo)

    mongosh "mongodb://localhost:27017"

    # create a database or switch to financialnews database

        use financialnews

    # create table (news_crawl_status) in financialnews database

        db.createCollection("news_crawl_status")

    # list all databases:

        show dbs

    # list all collections(tables) in the databse:

        show collections

    # query a collection(check the contents of a collection):

        db.news_crawl_status.find()

> > 4.  update local path

        in all cofig.py, update the two local paths
        in pipelines.py  update to local path        cls.file_dir = crawler.settings.get("FILE_DIR", "your local path")
        in settings.py # Update to local path        FILE_DIR = " your local path "

> > 5.  Crawl the news

    ```shell \
        cd news_crawler
        scrapy crawl financial_news
    ```

> > 5.  Generate the index

    ```
        cd news_indexer
        python news_index.py

    ```

> > 6.  Update Mongo

    ```
    # on mongosh create table news_crawl_status

        db.createCollection("news_crawl_status")
    ```

> > 7. check the backend on localhost

        cd APIs
        python app.py
        http://localhost:5600
        #specify a port:
        python app.py --port=5601

        #test query
        http://127.0.0.1:5601/query?text=YOUR_QUERY


    8. check the frontend
       nmp install
       nmp start run
=======
Copy .env.example to .env and fill in the required values before running the application.
>>>>>>> Mohitha
