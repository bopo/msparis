import Request from '../../utils/request';

export const getAddressList = data =>{
  return Request({
    url: '/user/address',
    method: 'GET',
    data,
  });
}
