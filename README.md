#async_function 

##socket - описана работа web-приложения на низком уровне. Сокет и роут.

##original.py - понятие о блокирующих функциях (остановка выполнения программы до получения результата из функции) - постановка проблемы

##1_event_loop.py - создание асинхронности (независимого вызова функций). select - для мониторинга

##2_selectors.py - создание асинхронности (независимого вызова функций). selectors - для мониторинга

##3_generators.py - Примеры генераторов, их возможности и создание Round Robins

##4_async_generators.py - создание асинхронности при помощи генераторных функций

##5_async_coroutines.py - понятие о корутинах (подпрограммах), декоратор

##6_delegations_generators.py - Делегирующий генератор - тот генератор, который вызывает другой генератор. Подгенератор - вызываемый генератор. Когда необходимо разбить один генератор на несколько
Конструкция yield from - управляет работой подгенератора. Можно не использовать инициализацию подгенератора, так как содержит в себе его инициализацию.