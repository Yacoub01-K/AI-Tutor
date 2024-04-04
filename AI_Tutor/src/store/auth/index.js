import mutation from './mutation';
import getter from './getter';

export default {
    namespaced: true,
    state() {
        return {
            authenticated: false,
            username: ""
        }
    },
    mutation,
    getter
}