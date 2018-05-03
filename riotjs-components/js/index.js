const Avatar = (email) => {
    const e = document.createElement('es-avatar');
    e.setAttribute('email', email);
    return e;
};

window.onload = () => {
    riot.mount('*');
    document.querySelector('body').appendChild(Avatar('dynamic@y.z'));
}