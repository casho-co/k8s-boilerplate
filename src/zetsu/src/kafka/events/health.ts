import { IEvent, logger, registerTopic } from '@cashoco/shared';
import TOPICS from '../config';

@registerTopic(TOPICS.HEALTH)
class Health {
  static consume_check_health(message: IEvent) {
    logger.info(`Message received by handler: ${message.data}`);
  }

  static produce_check_health() {
    return 'check_health';
  }
}

export default Health;
