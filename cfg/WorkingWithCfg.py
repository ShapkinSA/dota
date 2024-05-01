"""
    Парсинг файла конфигурации
"""
import xml.etree.ElementTree as ET
class WorkingWithCfg:

    @staticmethod
    def parsing_xml(xml_file_name):

        #Поиск по дереву конфигурационного файла
        tree = ET.parse(xml_file_name)
        root = tree.getroot()

        #Получаем конфиг scheduler
        scheduler_cfg = root.findall("scheduler")[0].attrib

        #Получаем конфиг мониторинга
        monitoring_cfg = root.findall("monitoring")[0].attrib

        #Получаем название стратегии
        strategy_name = root.findall("strategy")[0].attrib['name']

        #Находим нужный алгоритм стратегии
        strategy_cfg = root.findall(strategy_name)[0].attrib

        return scheduler_cfg, monitoring_cfg, strategy_cfg


