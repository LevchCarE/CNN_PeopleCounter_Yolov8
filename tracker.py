# Importación de la biblioteca math para cálculos matemáticos
import math


class Tracker:
    """
    Clase Tracker para el seguimiento de objetos en video.
    Implementa un sistema de seguimiento basado en la distancia entre centros de objetos.
    """
    def __init__(self):
        # Diccionario para almacenar los puntos centrales de los objetos
        # La clave es el ID del objeto y el valor es una tupla (x,y) del centro
        self.center_points = {}
        
        # Contador para asignar IDs únicos a nuevos objetos
        self.id_count = 0


    def update(self, objects_rect):
        """
        Actualiza el seguimiento de objetos basado en nuevos rectángulos detectados.
        
        Args:
            objects_rect: Lista de rectángulos detectados en el formato [x, y, w, h]
            
        Returns:
            objects_bbs_ids: Lista de rectángulos con sus IDs asignados [x, y, w, h, id]
        """
        # Lista para almacenar los rectángulos con sus IDs asignados
        objects_bbs_ids = []

        # Procesar cada nuevo rectángulo detectado
        for rect in objects_rect:
            x, y, w, h = rect
            # Calcular el punto central del rectángulo
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Verificar si este objeto ya fue detectado anteriormente
            same_object_detected = False
            for id, pt in self.center_points.items():
                # Calcular la distancia euclidiana entre el centro actual y el anterior
                dist = math.hypot(cx - pt[0], cy - pt[1])

                # Si la distancia es menor a 35 píxeles, consideramos que es el mismo objeto
                if dist < 35:
                    # Actualizar la posición del centro para este ID
                    self.center_points[id] = (cx, cy)
                    # Agregar el rectángulo con su ID a la lista de resultados
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # Si es un nuevo objeto, asignarle un nuevo ID
            if same_object_detected is False:
                # Guardar el nuevo punto central con un nuevo ID
                self.center_points[self.id_count] = (cx, cy)
                # Agregar el rectángulo con su nuevo ID
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                # Incrementar el contador de IDs
                self.id_count += 1

        # Limpiar el diccionario de puntos centrales
        # Eliminar IDs que ya no están siendo utilizados
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Actualizar el diccionario de puntos centrales
        self.center_points = new_center_points.copy()
        return objects_bbs_ids