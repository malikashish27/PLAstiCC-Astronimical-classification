# -*- coding: utf-8 -*-
"""xgboost model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iKlXn99P1pGqiZgX2Lt4AjxifBGyRHRj
"""

def main(argc, argv):
    # Features to compute with tsfresh library. Fft coefficient is meant to capture periodicity    
    
    # agg features
    aggs = {
        'flux': ['min', 'max', 'mean', 'median', 'std', 'skew'],
        'flux_err': ['min', 'max', 'mean', 'median', 'std', 'skew'],
        'detected': ['mean'],
        'flux_ratio_sq':['sum', 'skew'],
        'flux_by_flux_ratio_sq':['sum','skew'],
        'flux_det_pass_0-wise':['sum','skew'],
        'flux_det_pass_1-wise':['sum','skew'],
        'flux_det_pass_2-wise':['sum','skew'],
        'flux_det_pass_3-wise':['sum','skew'],
        'flux_det_pass_4-wise':['sum','skew'],
        'flux_det_pass_5-wise':['sum','skew'],
        'flux_det':['sum','skew'],
        'flux_err_det':['sum','skew'],
        'flux_ratio':['sum','skew'],
        'flux_by_flux_ratio':['sum','skew'],
        'flux_ratio_det_pass_0-wise':['sum','skew'],
        'flux_ratio_det_pass_1-wise':['sum','skew'],
        'flux_ratio_det_pass_2-wise':['sum','skew'],
        'flux_ratio_det_pass_3-wise':['sum','skew'],
        'flux_ratio_det_pass_4-wise':['sum','skew'],
        'flux_ratio_det_pass_5-wise':['sum','skew'],
        'flux_ratio_pass_0-wise':['sum','skew'],
        'flux_ratio_pass_1-wise':['sum','skew'],
        'flux_ratio_pass_2-wise':['sum','skew'],
        'flux_ratio_pass_3-wise':['sum','skew'],
        'flux_ratio_pass_4-wise':['sum','skew'],
        'flux_ratio_pass_5-wise':['sum','skew'],
        'mjd_det_pass_0-wise':['sum'],
        'mjd_det_pass_1-wise':['sum'],
        'mjd_det_pass_2-wise':['sum'],
        'mjd_det_pass_3-wise':['sum'],
        'mjd_det_pass_4-wise':['sum'],
        'mjd_det_pass_5-wise':['sum'],
        'mjd':['mean'],
        'relative_flux':['mean']
    }
    
    # tsfresh features
    fcp = {
        'flux': {
            'longest_strike_above_mean': None,
            'longest_strike_below_mean': None,
            'mean_change': None,
            'mean_abs_change': None,
            'length': None,
        },
                
        'flux_by_flux_ratio_sq': {
            'longest_strike_above_mean': None,
            'longest_strike_below_mean': None,       
        },
                
        'flux_passband': {
            'fft_coefficient': [
                    {'coeff': 0, 'attr': 'abs'}, 
                    {'coeff': 1, 'attr': 'abs'}
                ],
            'kurtosis' : None, 
            'skewness' : None,
        },
                
        'mjd': {
            'maximum': None, 
            'minimum': None,
            'mean_change': None,
            'mean_abs_change': None,
        },
    }
    best_params = {
        'objective': 'multi:softprob', 
        'eval_metric': 'mlogloss', 
        'silent': True, 
        'num_class': 14, 
        'booster': 'gbtree', 
        'n_jobs': -1, 
        'n_estimators': 1000, 
        'tree_method': 'hist', 
        'grow_policy': 'lossguide', 
        'max_depth': 7, 
        'base_score': 0.25, 
        'max_delta_step': 2, 
        'seed': 700, 
        'colsample_bytree': 0.3, 
        'gamma': 0.1, 
        'learning_rate': 0.02, 
        'max_leaves': 11, 
        'min_child_weight': 64, 
        'reg_alpha': 0.001, 
        'reg_lambda': 10.0, 
        'subsample': 0.9}
    
    meta_train = process_meta('../input/PLAsTiCC-2018/training_set_metadata.csv')
    
    train = pd.read_csv('../input/PLAsTiCC-2018/training_set.csv')
    full_train = featurize(train, meta_train, aggs, fcp)

    if 'target' in full_train:
        y = full_train['target']
        del full_train['target']
        
    classes = sorted(y.unique())    
    class_weights = {c: 1 for c in classes}
    class_weights.update({c:2 for c in [64, 15]})
    print('Unique classes : {}, {}'.format(len(classes), classes))
    print(class_weights)
    
    
    if 'object_id' in full_train:
        oof_df = full_train[['object_id']]
        del full_train['object_id'] 
        del full_train['ra'], full_train['decl'], full_train['gal_l'], full_train['gal_b']
        del full_train['ddf']
    
    pd.set_option('display.max_rows', 500)
    print(full_train.describe().T)
    full_train['flux_per_time_det_photoz']=(full_train['flux_det_sum'].values/full_train['mjd_diff_det'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_err_per_time_det_photoz']=(full_train['flux_err_det_sum'].values/full_train['mjd_diff_det'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_0_per_time_photoz']=(full_train['flux_det_pass_0-wise_sum'].values/full_train['mjd_det_pass_0-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_1_per_time_photoz']=(full_train['flux_det_pass_1-wise_sum'].values/full_train['mjd_det_pass_1-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_2_per_time_photoz']=(full_train['flux_det_pass_2-wise_sum'].values/full_train['mjd_det_pass_2-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_3_per_time_photoz']=(full_train['flux_det_pass_3-wise_sum'].values/full_train['mjd_det_pass_3-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_4_per_time_photoz']=(full_train['flux_det_pass_4-wise_sum'].values/full_train['mjd_det_pass_4-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['flux_det_pass_5_per_time_photoz']=(full_train['flux_det_pass_5-wise_sum'].values/full_train['mjd_det_pass_5-wise_sum'].values)*np.square(full_train['hostgal_photoz'].values)
    full_train['last_push']=full_train['mwebv']*np.square(full_train['hostgal_photoz'].values)
    full_train['distance']=full_train['hostgal_photoz'].values*full_train['mjd_mean'].values
    full_train['new_flux']=1/(full_train['distmod']**2)
         
    full_train['flux_amp_photoz'] = ((full_train['flux_max'].values-full_train['flux_min'].values)/full_train['flux_mean'].values)*np.square(full_train['hostgal_photoz'].values)
    del full_train['mjd_mean'], full_train['distmod'], full_train['mwebv'], full_train['hostgal_specz']
    full_train.fillna(-99999, inplace=True)
    print('shape:',full_train.shape)

    eval_func = partial(xgb_modeling_cross_validation, 
                        full_train=full_train, 
                        y=y, 
                        classes=classes, 
                        class_weights=class_weights, 
                        nr_fold=12, 
                        random_state=15)
    
    # modeling from CV
    clfs, score = eval_func(best_params)
        
    filename = 'subm_{:.6f}_{}.csv'.format(score, 
                     dt.now().strftime('%Y-%m-%d-%H-%M'))
    print('save to {}'.format(filename))
    # TEST
    z=process_test(clfs, 
                 features=full_train.columns, 
                 featurize_configs={'aggs': aggs, 'fcp': fcp}, 
                 train_mean=train_mean, 
                 filename=filename,
                 chunks=1000000,
                 nrows=range(1,150000000),
                 nrows2=150000000)
        
    print("Shape BEFORE grouping: {}".format(z.shape))
    z = z.groupby('object_id').mean()
    print("Shape AFTER grouping: {}".format(z.shape))
    return z.to_csv('single_{}'.format(filename), index=True)


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)