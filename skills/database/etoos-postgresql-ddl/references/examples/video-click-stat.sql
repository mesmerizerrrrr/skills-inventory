/**
    모의고사 해설영상 클릭 집계
    - 예상 데이터 건 수 : 연간 약 11,000 건씩 적재 예상 (61 개 지점 * 모의고사회당 약 20개영상 * 모의고사(서프) 연간 9번 시행)
    - 적재 시점 : redis 등으로 클릭 수 수집 후, 일 배치 스케줄러로 익일 자정 시간대에 수집된 redis 결과를 해당 테이블에 적재
 */
create table my247.tbl_mock_exam_explain_video_click_stat (
    vod_no    bigint       not null,
    brnch_cd  varchar(4)   not null,
    date      date         not null,
    clik_cnt  bigint       not null default 0,
    reger_id  varchar(50)  not null default 'SYSTEM',
    reg_dtm   timestamp(6) not null default now(),
    constraint pk_tbl_mock_exam_explain_video_click_stat primary key (vod_no, brnch_cd, date)
);
comment on table my247.tbl_mock_exam_explain_video_click_stat is '영상/지점 별 모의고사 해설영상 클릭 수 집계 (redis 우선 수집 후, 일 배치로 집계)';
comment on column my247.tbl_mock_exam_explain_video_click_stat.vod_no is '모의고사 해설영상 NO';
comment on column my247.tbl_mock_exam_explain_video_click_stat.brnch_cd is '지점 코드 (지점 별 클릭 수 집계)';
comment on column my247.tbl_mock_exam_explain_video_click_stat.date is '집계 기준 일자';
comment on column my247.tbl_mock_exam_explain_video_click_stat.clik_cnt is '클릭수';
comment on column my247.tbl_mock_exam_explain_video_click_stat.reger_id is '등록자 아이디';
comment on column my247.tbl_mock_exam_explain_video_click_stat.reg_dtm is '등록 일시';
-- DB 관리용 인덱스
create index idx_tbl_mock_exam_explain_video_click_stat_reg_dtm on my247.tbl_mock_exam_explain_video_click_stat(reg_dtm);