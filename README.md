#  💰 AI‑Powered  Cloud  Cost  Optimization Platform  (AWS  FinOps  + Bedrock)

This  project ingests  AWS  cost  data, analyzes  it,  and  uses **Amazon  Bedrock**  to  generate **human‑readable  optimization  recommendations**,  exposed via  a  REST  API and  a  **Next.js  dashboard**.

##  Components

-  **Infra  (Terraform)**  – S3,  DynamoDB,  Lambda,  IAM
-  **Backend**
   -  Cost  ingestion  Lambda (mocked  Athena  aggregation)
   -  AI  engine Lambda  (Bedrock‑powered  recommendations)
   -  API  Lambda (`/costs`,  `/recommendations`)
-  **Dashboard** –  Next.js  UI  for costs  &  recommendations

##  Quick  start

1.  Deploy  infra:

```bash
cd  infra/terraform
terraform init
terraform  apply  -var="region=us-east-1" -var="prefix=finops-demo"
