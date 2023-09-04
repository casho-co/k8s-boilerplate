import { IEvent, logger, registerTopic } from '@cashoco/shared';
import TOPICS from '../config';
import { User } from '../../models/user';

@registerTopic(TOPICS.HEALTH)
class Health {
  static consume_check_health(message: IEvent) {
    logger.info(`Message received by handler: ${message.data}`);
    const user = new User({
      name:'test',
      email:'test@test.com'
    })
    user.save().then(()=>{
      logger.info(`data added successfully`)
    }).catch((err)=>{
      logger.info(JSON.stringify(err))
    })
  }

  static produce_check_health() {
    return 'CHECK_HEALTH';
  }
}

export default Health;
