export let topicsRegistry: any = {};

export function registerTopic(topic: string) {
  return function (targetClass: Function) {
    topicsRegistry[topic] = targetClass;
  };
}
