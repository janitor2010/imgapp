export const setModalName = (state, { name }) => {
    state['showModal'] = name;
};

export const set = (state, { prop, val }) => {
    state[prop] = val;
};
