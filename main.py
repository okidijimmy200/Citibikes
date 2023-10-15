from prefect.infrastructure.docker import DockerContainer
from prefect.deployments import Deployment
from Flows.web_to_gcs import parent_flow
# from Flows.gcs_bigquery import big_query



docker_container_block = DockerContainer.load("citibikes-docker")

docker_depl = Deployment.build_from_flow(
    flow=parent_flow,
    name='docker-flow',
    infrastructure=docker_container_block
)



if __name__ == '__main__':
    months = [7, 8, 9, 10, 11, 12]
    year = 2013
    # parent_flow(year, months)
    # big_query(year, months)
    docker_depl.apply()

