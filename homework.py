from typing import Any, List


class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""
    k1: float = 18
    k2: float = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        cal_1 = self.k1 * self.get_mean_speed() - self.k2
        cal_2 = cal_1 * self.weight / self.M_IN_KM
        calories = cal_2 * (self.duration * self.MINS_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_c_1: float = 0.035
    cf_c_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        cal_1 = self.cf_c_1 * self.weight
        cal_2 = self.get_mean_speed()**2 // self.height
        cal_3 = cal_2 * self.cf_c_2 * self.weight
        calories = (cal_1 + cal_3) * self.duration * self.MINS_IN_HOUR
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    a1: float = 1.1
    a2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.count_pool = count_pool
        self.length_pool = length_pool

    def get_mean_speed(self) -> float:
        mean_speed_1 = self.length_pool * self.count_pool
        mean_speed = mean_speed_1 / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + self.a1) * self.a2 * self.weight
        return calories


def read_package(workout_type: str, data: List[Any]) -> Training:
    """Прочитать данные полученные от датчиков."""
    variants_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return variants_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
