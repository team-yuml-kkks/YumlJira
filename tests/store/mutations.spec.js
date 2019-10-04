import { expect } from 'chai';

import mutations from '../../client/store/mutations';

describe('Store mutations', () => {
    describe('logout', () => {
        const { logout } = mutations;

        it('Valid correct logout', () => {
            const state = {
                token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NywidXNlcm5hbWUiOiJrYW1pbDk5MiIsImV4cCI6MTU3MDM5NzI3MywiZW1haWwiOiJrYW1pbDk5MkBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2OTc5MjQ3M30.jI64xqY0K2MVd-eKdAhkEcjUlUFFS4WPhgNzqzK6eJQ',
                pk: 1,
                email: 'user@mail.com',
                username: 'user',
            };

            logout(state);

            expect(
                state.token,
                state.pk,
                state.email,
                state.username).to.be.null;
        });
    });

    describe('setUser', () => {
        const { setUser } = mutations;

        it('Set all user data and token', () => {
            const state = {
                token: null,
                pk: undefined,
                email: undefined,
                username: undefined,
            };

            const data = {
                token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NywidXNlcm5hbWUiOiJrYW1pbDk5MiIsImV4cCI6MTU3MDM5NzI3MywiZW1haWwiOiJrYW1pbDk5MkBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2OTc5MjQ3M30.jI64xqY0K2MVd-eKdAhkEcjUlUFFS4WPhgNzqzK6eJQ',
                user: {
                    pk: 1,
                    username: 'user',
                    email: 'user@gamil.com',
                }
            };

            setUser(state, { data });

            expect(state.token).to.equal(data.token);
            expect(state.pk).to.equal(data.user.pk);
            expect(state.username).to.equal(data.user.username);
            expect(state.email).to.equal(data.user.email);
        });
    });
});
