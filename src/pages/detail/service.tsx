import Request from '../../utils/request';

// 获取商品详情
export const getProductInfo = params =>{
  return Request({
    url: '/product',
    method: 'GET',
    data: params,
  });
}