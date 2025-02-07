import calendar
import datetime
import time

from hydrus.core import HydrusData
from hydrus.core import HydrusConstants as HC

def DateTimeToTimestamp( dt: datetime.datetime ) -> int:
    
    try:
        
        timestamp = int( dt.timestamp() )
        
    except:
        
        try:
            
            # ok bros, an important thing about time.mktime and datetime.timestamp is they can't always handle <1970!
            # so we'll do some mickey mouse stuff here and this does work
            
            dt_epoch = datetime.datetime( 1970, 1, 1, tzinfo = datetime.timezone.utc )
            
            # we would want to go dt_local = dt.astimezone(), but we can't do astimezone on a dt with pre-1970 date
            # but we can mess around it. and if an hour of DST is miscalculated fifty years ago, oh well!
            my_current_timezone = datetime.datetime.now().astimezone().tzinfo
            
            dt_local = datetime.datetime(
                year = dt.year,
                month = dt.month,
                day = dt.day,
                hour = dt.hour,
                minute = dt.minute,
                second = dt.second,
                tzinfo = my_current_timezone
            )
            
            time_delta = dt_local - dt_epoch
            
            timestamp = int( time_delta.total_seconds() )
            
        except:
            
            timestamp = GetNow()
            
        
    
    return timestamp
    

def GetDateTime( year: int, month: int, day: int, hour: int, minute: int ) -> datetime.datetime:
    
    return datetime.datetime( year, month, day, hour, minute )
    

def GetNow():
    
    return int( time.time() )
    

def GetNowFloat():
    
    return time.time()
    

def GetNowPrecise():
    
    return time.perf_counter()
    

def GetTimeDeltaSinceTime( timestamp ):
    
    time_since = timestamp - GetNow()
    
    result = min( time_since, 0 )
    
    return - result
    

def GetTimeDeltaUntilTime( timestamp ):
    
    time_remaining = timestamp - GetNow()
    
    return max( time_remaining, 0 )
    

def GetTimeDeltaUntilTimeFloat( timestamp ):
    
    time_remaining = timestamp - GetNowFloat()
    
    return max( time_remaining, 0.0 )
    

def GetTimeDeltaUntilTimePrecise( t ):
    
    time_remaining = t - GetNowPrecise()
    
    return max( time_remaining, 0.0 )
    

def TimeHasPassed( timestamp ):
    
    if timestamp is None:
        
        return False
        
    
    return GetNow() > timestamp
    

def TimeHasPassedFloat( timestamp ):
    
    return GetNowFloat() > timestamp
    

def TimeHasPassedPrecise( precise_timestamp ):
    
    return GetNowPrecise() > precise_timestamp
    

def TimeUntil( timestamp ):
    
    return timestamp - GetNow()
    

def CalendarDeltaToDateTime( years : int, months : int, days : int, hours : int ) -> datetime.datetime:
    
    now = datetime.datetime.now()
    
    day_and_hour_delta = datetime.timedelta( days = days, hours = hours )
    
    result = now - day_and_hour_delta
    
    new_year = result.year - years
    new_month = result.month - months
    
    while new_month < 1:
        
        new_year -= 1
        new_month += 12
        
    
    while new_month > 12:
        
        new_year += 1
        new_month -= 12
        
    
    try:
        
        dayrange = calendar.monthrange( new_year, new_month )
        
    except:
        
        dayrange = ( 0, 30 )
        
    
    new_day = min( dayrange[1], result.day )
    
    result = datetime.datetime(
        year = new_year,
        month = new_month,
        day = new_day,
        hour = result.hour,
        minute = result.minute,
        second = result.second
    )
    
    return result
    

def CalendarDeltaToRoughDateTimeTimeDelta( years : int, months : int, days : int, hours : int ) -> datetime.timedelta:
    
    return datetime.timedelta( days = days + ( months * ( 365.25 / 12 ) ) + ( years * 365.25 ), hours = hours )
    

def TimeDeltaToPrettyTimeDelta( seconds, show_seconds = True, no_bigger_than_days = False ):
    
    if seconds is None:
        
        return 'per month'
        
    
    if seconds == 0:
        
        return '0 seconds'
        
    
    if seconds < 0:
        
        seconds = abs( seconds )
        
    
    if seconds >= 60:
        
        seconds = int( seconds )
        
        MINUTE = 60
        HOUR = 60 * MINUTE
        DAY = 24 * HOUR
        YEAR = 365.25 * DAY
        MONTH = YEAR / 12
        
        lines = []
        
        if not no_bigger_than_days:
            
            lines.append( ( 'year', YEAR ) )
            lines.append( ( 'month', MONTH ) )
            
        
        lines.append( ( 'day', DAY ) )
        lines.append( ( 'hour', HOUR ) )
        lines.append( ( 'minute', MINUTE ) )
        
        if show_seconds:
            
            lines.append( ( 'second', 1 ) )
            
        
        result_components = []
        
        for ( time_string, duration ) in lines:
            
            time_quantity = seconds // duration
            
            seconds %= duration
            
            # little rounding thing if you get 364th day with 30 day months
            if time_string == 'month' and time_quantity > 11:
                
                time_quantity = 11
                
            
            if time_quantity > 0:
                
                s = HydrusData.ToHumanInt( time_quantity ) + ' ' + time_string
                
                if time_quantity > 1:
                    
                    s += 's'
                    
                
                result_components.append( s )
                
                if len( result_components ) == 2: # we now have 1 month 2 days
                    
                    break
                    
                
            else:
                
                if len( result_components ) > 0: # something like '1 year' -- in which case we do not care about the days and hours
                    
                    break
                    
                
            
        
        result = ' '.join( result_components )
        
    elif seconds > 1:
        
        if int( seconds ) == seconds:
            
            result = HydrusData.ToHumanInt( seconds ) + ' seconds'
            
        else:
            
            result = '{:.1f} seconds'.format( seconds )
            
        
    elif seconds == 1:
        
        result = '1 second'
        
    elif seconds > 0.1:
        
        result = '{} milliseconds'.format( int( seconds * 1000 ) )
        
    elif seconds > 0.01:
        
        result = '{:.1f} milliseconds'.format( int( seconds * 1000 ) )
        
    elif seconds > 0.001:
        
        result = '{:.2f} milliseconds'.format( int( seconds * 1000 ) )
        
    else:
        
        result = '{} microseconds'.format( int( seconds * 1000000 ) )
        
    
    return result
    

def TimestampToDateTime( timestamp, timezone = None ) -> datetime.datetime:
    
    if timezone is None:
        
        timezone = HC.TIMEZONE_LOCAL
        
    
    # ok we run into the <1970 problems again here. time.gmtime may just fail for -12345678
    # therefore we'll meme it up by adding our timestamp as a delta, which works
    # ALSO NOTE YOU CAN MESS UP IN TWENTY WAYS HERE. if you try to do dt.astimezone() on a certain date, you'll either get standard or daylight timezone lmao!
    dt_epoch = datetime.datetime( 1970, 1, 1 )
    
    dt = dt_epoch + datetime.timedelta( seconds = timestamp )
    
    if timezone == HC.TIMEZONE_LOCAL:
        
        my_current_timezone = datetime.datetime.now().astimezone().tzinfo
        
        my_offset_timedelta = my_current_timezone.utcoffset( None )
        
        dt += my_offset_timedelta
        
    
    return dt
    

def TimestampToPrettyExpires( timestamp ):
    
    if timestamp is None:
        
        return 'does not expire'
        
    
    if timestamp == 0:
        
        return 'unknown expiration'
        
    
    try:
        
        time_delta_string = TimestampToPrettyTimeDelta( timestamp )
        
        if TimeHasPassed( timestamp ):
            
            return 'expired ' + time_delta_string
            
        else:
            return 'expires ' + time_delta_string
            
        
    except:
        
        return 'unparseable time {}'.format( timestamp )
        
    

def MillisecondsToPrettyTime( ms ):
    
    hours = ms // 3600000
    
    if hours == 1: hours_result = '1 hour'
    else: hours_result = str( hours ) + ' hours'
    
    ms = ms % 3600000
    
    minutes = ms // 60000
    
    if minutes == 1: minutes_result = '1 minute'
    else: minutes_result = str( minutes ) + ' minutes'
    
    ms = ms % 60000
    
    seconds = ms // 1000
    
    if seconds == 1: seconds_result = '1 second'
    else: seconds_result = str( seconds ) + ' seconds'
    
    detailed_seconds = ms / 1000
    
    detailed_seconds_result = '{:.1f} seconds'.format( detailed_seconds )
    
    ms = ms % 1000
    
    if hours > 0: return hours_result + ' ' + minutes_result
    
    if minutes > 0: return minutes_result + ' ' + seconds_result
    
    if seconds > 0: return detailed_seconds_result
    
    ms = int( ms )
    
    if ms == 1: milliseconds_result = '1 millisecond'
    else: milliseconds_result = '{} milliseconds'.format( ms )
    
    return milliseconds_result
    

def TimestampToPrettyTime( timestamp, in_utc = False, include_24h_time = True ):
    
    if timestamp is None:
        
        return 'unknown time'
        
    
    if include_24h_time:
        
        phrase = '%Y-%m-%d %H:%M:%S'
        
    else:
        
        phrase = '%Y-%m-%d'
        
    
    if in_utc:
        
        timezone = HC.TIMEZONE_UTC
        
    else:
        
        timezone = HC.TIMEZONE_LOCAL
        
    
    try:
        
        dt = TimestampToDateTime( timestamp, timezone = timezone )
        
        return dt.strftime( phrase )
        
    except:
        
        return 'unparseable time {}'.format( timestamp )
        
    

def BaseTimestampToPrettyTimeDelta( timestamp, just_now_string = 'now', just_now_threshold = 3, history_suffix = ' ago', show_seconds = True, no_prefix = False ):
    
    if timestamp is None:
        
        return 'at an unknown time'
        
    
    if not show_seconds:
        
        just_now_threshold = max( just_now_threshold, 60 )
        
    
    try:
        
        time_delta = abs( timestamp - GetNow() )
        
        if time_delta <= just_now_threshold:
            
            return just_now_string
            
        
        time_delta_string = TimeDeltaToPrettyTimeDelta( time_delta, show_seconds = show_seconds )
        
        if TimeHasPassed( timestamp ):
            
            return '{}{}'.format( time_delta_string, history_suffix )
            
        else:
            
            if no_prefix:
                
                return time_delta_string
                
            else:
                
                return 'in ' + time_delta_string
                
            
        
    except:
        
        return 'unparseable time {}'.format( timestamp )
        
    

TimestampToPrettyTimeDelta = BaseTimestampToPrettyTimeDelta

def ValueRangeToScanbarTimestampsMS( value_ms, range_ms ):
    
    value_ms = int( round( value_ms ) )
    
    range_hours = range_ms // 3600000
    value_hours = value_ms // 3600000
    range_minutes = ( range_ms % 3600000 ) // 60000
    value_minutes = ( value_ms % 3600000 ) // 60000
    range_seconds = ( range_ms % 60000 ) // 1000
    value_seconds = ( value_ms % 60000 ) // 1000
    range_ms = range_ms % 1000
    value_ms = value_ms % 1000
    
    if range_hours > 0:
        
        # 0:01:23.033/1:12:57.067
        
        time_phrase = '{}:{:0>2}:{:0>2}.{:0>3}'
        
        args = ( value_hours, value_minutes, value_seconds, value_ms, range_hours, range_minutes, range_seconds, range_ms )
        
    elif range_minutes > 0:
        
        # 01:23.033/12:57.067 or 0:23.033/1:57.067
        
        if range_minutes > 9:
            
            time_phrase = '{:0>2}:{:0>2}.{:0>3}'
            
        else:
            
            time_phrase = '{:0>1}:{:0>2}.{:0>3}'
            
        
        args = ( value_minutes, value_seconds, value_ms, range_minutes, range_seconds, range_ms )
        
    else:
        
        # 23.033/57.067 or 3.033/7.067 or 0.033/0.067
        
        if range_seconds > 9:
            
            time_phrase = '{:0>2}.{:0>3}'
            
        else:
            
            time_phrase = '{:0>1}.{:0>3}'
            
        
        args = ( value_seconds, value_ms, range_seconds, range_ms )
        
    
    full_phrase = '{}/{}'.format( time_phrase, time_phrase )
    
    result = full_phrase.format( *args )
    
    return result
