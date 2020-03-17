DOCKER_IMAGE_NAME=mailchimp-service

.PHONY: deploy
deploy:
	@docker start awsecr
	@docker exec -ti awsecr pull $(DOCKER_IMAGE_NAME)
	docker-compose up -d
	@docker system prune -f --filter 'label=cgsy.image.name=mailchimp-service'
