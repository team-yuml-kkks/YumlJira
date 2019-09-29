import { expect } from 'chai';

import mutations from '../../client/store/mutations';
import storeState from '../../client/store/state';

describe('Store mutations', () => {
    describe('logout', () => {
        const { logout } = mutations;

        it('Clear all critical stored data', () => {
            const state = {
                token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NywidXNlcm5hbWUiOiJrYW1pbDk5MiIsImV4cCI6MTU3MDM5NzI3MywiZW1haWwiOiJrYW1pbDk5MkBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2OTc5MjQ3M30.jI64xqY0K2MVd-eKdAhkEcjUlUFFS4WPhgNzqzK6eJQ',
                pk: 1,
                email: 'user@mail.com',
                username: 'user',
            };
            logout(state);
            expect(
                storeState.token,
                storeState.pk,
                storeState.email,
                storeState.username).to.null;
        });
    });

    describe('setUser', () => {
        const { setUser } = mutations;

        it('Set all user data and token', () => {
            const state = {
                token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0NywidXNlcm5hbWUiOiJrYW1pbDk5MiIsImV4cCI6MTU3MDM5NzI3MywiZW1haWwiOiJrYW1pbDk5MkBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU2OTc5MjQ3M30.jI64xqY0K2MVd-eKdAhkEcjUlUFFS4WPhgNzqzK6eJQ',
                pk: 1,
                email: 'user@mail.com',
                username: 'user',
            };
            setUser(state);
            expect(
                storeState.token,
                storeState.pk,
                storeState.email,
                storeState.username).not.null;
        });
    });
});
