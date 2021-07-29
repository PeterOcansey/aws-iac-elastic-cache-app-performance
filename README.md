## Improve Application Performance using Amazon ElasticCache

### Database
- To spin up your database, use `iac-rds-pgsql.yml` and `iac-rds-params.json` files
- Update values in `iac-rds-params.json` to suite your need
- From your terminal, execute `bash bash_scripts/create.sh 'your_stack_name_here'  iac-rds-pgsql.yml iac-rds-params.json` to spin up your Amazon RDS PostgreSQL database.


### Application
- To spin up your database, use `iac-app-server.yml` and `iac-app-server-params.json` files
- Update values in `iac-app-server-params.json` to suite your need
- From your terminal, execute `bash bash_scripts/create.sh 'your_stack_name_here'  iac-app-server.yml iac-app-server-params.json` to spin up your EC2 instance and get your application up and running


### Cache
- To spin up your redis elastic cache cluster, use `iac-elastic-cache.yml` and `iac-elastic-cache-params.json` files
- Update values in `iac-elastic-cache-params.json` to suite your need
- From your terminal, execute `bash bash_scripts/create.sh 'your_stack_name_here'  iac-elastic-cache.yml iac-elastic-cache-params.json` to spin up your Redis ElastiCache Cluster up and running




