from apps.soltura.dto.soltura_dtos import CursorDTO

class CursorPaginator:

    @staticmethod
    def paginar(qs, limit):
        rows = list(qs[: limit + 1])
        next_cursor = None

        if len(rows) > limit:
            last = rows.pop()
            next_cursor = CursorDTO(
                id=last.id,
                data_soltura=str(last.data_soltura)
            )

        return rows, next_cursor