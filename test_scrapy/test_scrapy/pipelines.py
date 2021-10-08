# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from .pgdb import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from .SQLalchemy_classes import *
from .spiders.authors import *
from .spiders.author_details import *


class DeleteQuotes:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['quote'] = re.sub('''[\“\”]+''', '', adapter['quote'])
        return item


class DeleteNewLine:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['quote'] = re.sub('''[\n]+''', '', adapter['quote'])
        return item


class SaveToPostgres:

    def open_spider(self, spider):
        DBSession = sessionmaker(bind=engine)
        Base.metadata.bind = engine
        self.session = DBSession()

    def close_spider(self, spider):
        self.session.close()

    def author_exist(self, author):
        res = self.session.query(Author.name, Author.author_id).filter(Author.name == author).first()
        if res is not None:
            return res.author_id
        else:
            return res

    def keyword_exist(self, keyword):
        res = self.session.query(Keyword.keyword, Keyword.keyword_id).filter(Keyword.keyword == keyword).first()
        if res is not None:
            return res.keyword_id
        else:
            return res

    def save_keyword(self, keyword):
        id_ = self.keyword_exist(keyword)
        if id_ is None:
            try:
                keyword_ = Keyword(keyword=keyword)
                self.session.add(keyword_)
                self.session.commit()
                id_ = keyword_.keyword_id
            except Exception as e:
                print(f'There is an Exception {e}')
            finally:
                self.session.rollback()
        return id_

    def save_author(self, item):
        adapter = ItemAdapter(item)
        id_ = self.author_exist(adapter['author'])
        if id_ is None:
            try:
                author_ = Author(name=adapter['author'], link=adapter['link'])
                self.session.add(author_)
                self.session.commit()
                id_ = author_.author_id
            except Exception as e:
                print(f'There is an Exception {e}')
            finally:
                self.session.rollback()
        return id_

    def save_quote(self, item, author_id):
        adapter = ItemAdapter(item)
        id_ = None
        try:
            quote_ = Quote(quote=adapter['quote'], author_id=author_id)
            self.session.add(quote_)
            self.session.commit()
            id_ = quote_.quote_id
        except Exception as e:
            print(f'There is an Exception {e}')
        finally:
            self.session.rollback()
        return id_

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        author_id = self.save_author(item)
        quote_id = self.save_quote(item, author_id)
        if None not in [author_id, quote_id]:
            for keyword in adapter['keywords']:
                keyword_id_ = self.save_keyword(keyword)
                union_ = Keywords_and_quotes(keyword_id=keyword_id_,
                                             quote_id=quote_id
                                             )
                self.session.add(union_)
                self.session.commit()
        return item


class StripClearItem:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["author"] = adapter["author"].strip()
        adapter["info"] = adapter["info"].strip()
        adapter["author"] = re.sub('\-', ' ', adapter["author"])
        return item


class SaveAuthorDetails:

    def open_spider(self, spider):
        DBSession = sessionmaker(bind=engine)
        Base.metadata.bind = engine
        self.session = DBSession()

    def close_spider(self, spider):
        self.session.close()

    def author_exist(self, author):
        res = self.session.query(Author.name, Author.author_id).filter(Author.name == author).first()
        if res is not None:
            return res.author_id
        else:
            return res

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['author'] = re.sub('''[\n]+''', '', adapter['author'])
        adapter['info'] = re.sub('''[\n]+''', '', adapter['info'])
        author_id = self.author_exist(adapter['author'])
        if author_id is not None:
            try:
                self.session.execute(
                    update(Author, values={
                        Author.birthday: adapter['birthday'],
                        Author.author_info: adapter['info']
                    }
                    ).filter(Author.author_id == author_id)
                )
                self.session.commit()
            except Exception as e:
                print(f'There is an Exception {e}')
            finally:
                self.session.rollback()
        return item
