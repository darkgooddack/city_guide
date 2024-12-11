-- Создание таблицы kitchen
CREATE TABLE IF NOT EXISTS kitchen (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы food_place
CREATE TABLE IF NOT EXISTS food_place (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    address VARCHAR(255),
    link_map VARCHAR(255),
    time VARCHAR(50),
    budget INTEGER
);

-- Создание промежуточной таблицы food_place_kitchen для связи кухонь с местами питания
CREATE TABLE IF NOT EXISTS food_place_kitchen (
    id SERIAL PRIMARY KEY,
    food_place_id INTEGER NOT NULL,
    kitchen_id INTEGER NOT NULL,
    FOREIGN KEY (food_place_id) REFERENCES food_place(id) ON DELETE CASCADE,
    FOREIGN KEY (kitchen_id) REFERENCES kitchen(id) ON DELETE CASCADE
);


-- Вставка данных в таблицу kitchen
INSERT INTO kitchen (name) VALUES
('Французская'),
('Испанская'),
('Русская')
('Индийская'),
('Китайская'),
('Японская');

-- Вставка данных в таблицу food_place
INSERT INTO food_place (name, description, address, link_map, time, budget) VALUES
('Ресторан Тихий Дон', 'Традиционная кухня с видом на реку Дон', 'Береговая ул., 10', 'https://yandex.by/maps/org/tikhiy_don/122784573045/?filter=alternate_vertical%3ARequestWindow&ll=39.708967%2C47.213019&mode=search&sctx=ZAAAAAgBEAAaKAoSCdfZkH9m0ENAEef%2FVUeOoEdAEhIJ5dL4hVeS3D8RbHh6pSzD4z8iBgABAgMEBSgKOABAlVZIAWoCdWGdAc3MzD2gAQCoAQC9ARTjbS7CAQb1zJ%2B0yQOCAj7QoNC%2B0YHRgtC%2B0LIg0L3QsCDQlNC%2B0L3Rgywg0YDQtdGB0YLQvtGA0LDQvSDRgtC40YXQuNC5INC00L7QvYoCAJICAjM5mgIMZGVza3RvcC1tYXBz&sll=39.708967%2C47.213019&sspn=0.027902%2C0.038629&text=%D0%A0%D0%BE%D1%81%D1%82%D0%BE%D0%B2%20%D0%BD%D0%B0%20%D0%94%D0%BE%D0%BD%D1%83%2C%20%D1%80%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%20%D1%82%D0%B8%D1%85%D0%B8%D0%B9%20%D0%B4%D0%BE%D0%BD&z=13.8', '10:00 - 23:00', 2000),
('Sapore Italiano', 'Итальянская пицца', 'просп. Соколова, 17', 'https://yandex.by/maps/org/sapore_italiano/3491092269/?ll=39.720941%2C47.223345&mode=search&sctx=ZAAAAAgBEAAaKAoSCbx4P26%2F2kNAEZw24zREm0dAEhIJ5dL4hVeSnD8R3LdaJy7Hoz8iBgABAgMEBSgKOABAh80GSAFqAnVhnQHNzMw9oAEAqAEAvQFpNTbOggI%2B0JvRg9GH0YjQuNC1INC40YLQsNC70YzRj9C90YHQutC40LUg0L%2FQuNGG0YbRiyDQsiDQs9C%2B0YDQvtC00LWKAgCSAgCaAgxkZXNrdG9wLW1hcHPCAgPigr0%3D&sll=39.720941%2C47.223345&sspn=2.323841%2C3.216679&text=%D0%9B%D1%83%D1%87%D1%88%D0%B8%D0%B5%20%D0%B8%D1%82%D0%B0%D0%BB%D1%8C%D1%8F%D0%BD%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%B8%D1%86%D1%86%D1%8B%20%D0%B2%20%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%B5&z=7.42', '12:00 - 22:00', 1500);
('Кафе Кавказский дворик', 'Аутентичные блюда Кавказской кухни', 'просп. Космонавтов, 2/3', 'https://yandex.by/maps/org/kavkazskiy_dvorik/214081190742/?ll=39.622136%2C47.292822&mode=search&sctx=ZAAAAAgBEAAaKAoSCTuscMtH3ENAEdFcp5GWnEdAEhIJ3NRA8zmXAkARAtcVM8K7CUAiBgABAgMEBSgKOABAkE5IAWoCdWGdAc3MzD2gAQCoAQC9AVph%2BgnCAWzd9d%2BtBI2zi43HBsa%2F7IueAou%2Bmd8DxIC4nQT6mun2ugHT3eOJ0QTL87CPZLnqnrz6AYLakKW9BsWk%2FKjHBZjFltymAsGdnrHfBpny1uTHBoOp5fvdBcPFjoDRBaiUk7Nqo4G1%2FvsB2d%2Fp1QaCAirQmtCw0YTQtSDQmtCw0LLQutCw0LfRgdC60LjQuSDQtNCy0L7RgNC40LqKAgCSAgCaAgxkZXNrdG9wLW1hcHOqAgsxNTYzMjE3NzU2OLACAQ%3D%3D&sll=39.622136%2C47.292822&sspn=0.378014%2C0.522546&text=%D0%9A%D0%B0%D1%84%D0%B5%20%D0%9A%D0%B0%D0%B2%D0%BA%D0%B0%D0%B7%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%B2%D0%BE%D1%80%D0%B8%D0%BA&z=10.04', '11:00 - 00:00', 1800);

-- Вставка данных в промежуточную таблицу food_place_kitchen
INSERT INTO food_place_kitchen (food_place_id, kitchen_id) VALUES
(1, 3),
(2, 3),
(3, 2),
(1, 2),
(1, 1),
(2, 4);
