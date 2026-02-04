def get_costs():
       data  =  [
             {"date":  "2026-02-01",  "service":  "Amazon EC2",  "cost":  120.5},
              {"date": "2026-02-01",  "service":  "Amazon  RDS", "cost":  80.2},
              {"date":  "2026-02-01", "service":  "Amazon  S3",  "cost": 45.7},
       ]
       return  {"items": data},  200
