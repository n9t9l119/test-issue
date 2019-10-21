Перед запуском скрипта необходимо установить зависимости среды 
(команда pip install -r requirements.txt)

HTTP-сервер содержит следующие API-запросы:
1)http://localhost:port/api/sendMessage (метод "POST")
2)http://localhost:port/api/sendMessage/<file_path> (метод "GET"), где file_path - путь к файлу,
содержащему сообщение в XML-формате
3)http://localhost:port/api/getMessage (метод "GET")
4)http://localhost:port/api/findMessages (метод "POST")