from rest_framework.views import APIView
from rest_framework.response import Response
from .data import DATA, CLOSURE_DATA, BLOCKAGE_DATA


class DummyAPI(APIView):
    """Single endpoint that returns combined data by default.

    Behavior:
      - GET /api/dummy/                     => returns combined list `DATA` (all records)
      - GET /api/dummy/?kind=closure         => returns only closure records
      - GET /api/dummy/?kind=blockage        => returns only blockage records
      - GET /api/dummy/closure/              => returns only closure records (path param)
      - GET /api/dummy/blockage/             => returns only blockage records (path param)

    If you need grouped output (closures/blockages as separate keys) use
    `?grouped=true` and the response will be `{"closures": [...], "blockages": [...]}`.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, kind: str = None):
        # accept kind either from path param or query param
        if not kind:
            kind = request.query_params.get("kind")

        # grouped response requested?
        grouped = request.query_params.get("grouped") in ("1", "true", "True")

        if not kind:
            # no kind specified -> return combined DATA list
            if grouped:
                return Response({"closures": CLOSURE_DATA, "blockages": BLOCKAGE_DATA})
            return Response(DATA)

        kind = kind.lower()
        if kind in ("closure", "closures"):
            return Response(CLOSURE_DATA)
        if kind in ("blockage", "blockages"):
            return Response(BLOCKAGE_DATA)

        return Response({"error": "invalid kind - use 'closure' or 'blockage'"}, status=400)
