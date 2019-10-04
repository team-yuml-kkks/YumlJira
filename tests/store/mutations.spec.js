import { expect } from 'chai';

import mutations from '../../client/store/mutations';

describe('Store mutations', () => {
    describe('logout', () => {
        const { logout } = mutations;

        it('Correctly logouts user', () => {
            const state = {
                token: 'test',
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

        it('Sets all user data and token', () => {
            const state = {
                token: null,
                pk: undefined,
                email: undefined,
                username: undefined,
            };

            const data = {
                token: 'test',
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
