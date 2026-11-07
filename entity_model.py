"""Этап 1 (Вариант Б): Моделирование пакета телеметрии куста, сохранение и чтение JSON."""
import json
import subprocess
from typing import Any

def get_git_username() -> str:
    """Автоматически получает имя пользователя из глобальных настроек Git."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"], 
            capture_output=True, 
            text=True, 
            check=True,
            encoding="utf-8"
        )
        username = result.stdout.strip()
        return username if username else "Неизвестный автор"
    except (subprocess.SubprocessError, FileNotFoundError):
        return "Студент"

def build_telemetry_packet() -> dict[str, Any]:
    """Формирует пакет телеметрии со списком датчиков по индивидуальным числам пары (для N=8)."""
    return {
        "pad_id": "PAD-18",
        "well_id": "W-208",
        "p_res_mpa": 26.0,
        "p_bhp_mpa": 15.2,
        "mode": "PUMPING",
        "is_online": True,  # Добавлено в Челлендже №1
        "author": get_git_username(),
        "sensors": [
            {"code": "T-01", "value": 57.0, "unit": "C"},
            {"code": "Q-01", "value": 92.0, "unit": "m3/d"},
            {"code": "P-01", "value": 14.0, "unit": "MPa"}  # Добавлено в Челлендже №1
        ],
    }

def save_to_json(data: dict[str, Any], filename: str = "data.json") -> None:
    """Сериализует пакет телеметрии в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_from_json(filename: str = "data.json") -> dict[str, Any]:
    """Читает JSON-файл с диска обратно в словарь Python."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def print_telemetry_summary(packet: dict[str, Any]) -> None:
    """Выводит сводку по пакету телеметрии и считает депрессию на пласт."""
    drawdown = packet["p_res_mpa"] - packet["p_bhp_mpa"]
    print("=" * 58)
    print(f"ПАКЕТ ТЕЛЕМЕТРИИ: Куст {packet['pad_id']} | Скважина {packet['well_id']}")
    print(f"Статус связи: {'ONLINE' if packet['is_online'] else 'OFFLINE'} | Автор: {packet.get('author')}")
    print("=" * 58)
    print(f"Режим работы: {packet['mode']}")
    print(f"Давления: Pпл = {packet['p_res_mpa']} МПа, Pзаб = {packet['p_bhp_mpa']} МПа (dP = {drawdown:.2f} МПа)")
    print(f"Опрошено датчиков: {len(packet['sensors'])} шт.")
    for s in packet["sensors"]:
        print(f" -> Датчик {s['code']}: {s['value']} {s['unit']}")
    print("=" * 58)

if __name__ == "__main__":
    pkt = build_telemetry_packet()
    save_to_json(pkt, "data.json")
    print("[OK] Файл 'data.json' успешно записан на диск!")
    
    loaded_pkt = load_from_json("data.json")
    assert loaded_pkt == pkt, "Ошибка: данные при чтении JSON исказились!"
    print("[OK] Обратное чтение через json.load() прошло успешно!\n")
    
    print_telemetry_summary(loaded_pkt)